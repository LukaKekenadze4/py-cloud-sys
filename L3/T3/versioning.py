# Run: python L3/T3/versioning.py my-bucket-name -vs
#      python L3/T3/versioning.py my-bucket-name file.txt -lv
#      python L3/T3/versioning.py my-bucket-name file.txt -rp

import argparse

import boto3
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("bucket_name")
parser.add_argument("key", nargs="?", help="File name (Key), needed for -lv and -rp")
parser.add_argument("-vs", "--versioning-status", action="store_true",
                    help="Show whether versioning is enabled on the bucket")
parser.add_argument("-lv", "--list-versions", action="store_true",
                    help="Show the number of versions of the file and their dates")
parser.add_argument("-rp", "--restore-previous", action="store_true",
                    help="Upload the previous version of the file as a new version")
args = parser.parse_args()

if (args.list_versions or args.restore_previous) and not args.key:
    parser.error("file name (key) is required for -lv and -rp")

s3 = boto3.client("s3")


def get_versions(bucket_name, key):
    response = s3.list_object_versions(Bucket=bucket_name, Prefix=key)
    # newest first; Prefix can also match other files, so filter by exact key
    return [v for v in response.get("Versions", []) if v["Key"] == key]


if args.versioning_status:
    status = s3.get_bucket_versioning(Bucket=args.bucket_name).get("Status")
    print(f"Versioning: {status or 'Not enabled'}")

if args.list_versions:
    versions = get_versions(args.bucket_name, args.key)
    print(f"Versions: {len(versions)}")
    for version in versions:
        print(f"  {version['LastModified']}  {version['VersionId']}")

if args.restore_previous:
    versions = get_versions(args.bucket_name, args.key)
    if len(versions) < 2:
        print("No previous version")
    else:
        previous = versions[1]
        s3.copy_object(
            Bucket=args.bucket_name,
            Key=args.key,
            CopySource={"Bucket": args.bucket_name, "Key": args.key,
                        "VersionId": previous["VersionId"]},
        )
        print(f"Previous version ({previous['LastModified']}) uploaded as a new version")
