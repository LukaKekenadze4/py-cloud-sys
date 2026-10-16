# Run: python L3/T3/versioning.py my-bucket -vs
#      python L3/T3/versioning.py my-bucket file.txt -lv
#      python L3/T3/versioning.py my-bucket file.txt -rp

import argparse

import boto3
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("bucket_name")
parser.add_argument("key", nargs="?")
parser.add_argument("-vs", action="store_true", help="is versioning enabled")
parser.add_argument("-lv", action="store_true", help="list file versions")
parser.add_argument("-rp", action="store_true", help="restore previous version")
args = parser.parse_args()

if (args.lv or args.rp) and not args.key:
    parser.error("file name is required for -lv and -rp")

s3 = boto3.client("s3")

if args.vs:
    status = s3.get_bucket_versioning(Bucket=args.bucket_name).get("Status")
    print(f"Versioning: {status or 'Not enabled'}")

if args.lv or args.rp:
    response = s3.list_object_versions(Bucket=args.bucket_name, Prefix=args.key)
    # newest first; Prefix also matches other files, so keep only the exact key
    versions = [v for v in response.get("Versions", []) if v["Key"] == args.key]

if args.lv:
    print(f"Versions: {len(versions)}")
    for v in versions:
        print(f"  {v['LastModified']}  {v['VersionId']}")

if args.rp:
    if len(versions) < 2:
        print("No previous version")
    else:
        s3.copy_object(
            Bucket=args.bucket_name,
            Key=args.key,
            CopySource={"Bucket": args.bucket_name, "Key": args.key,
                        "VersionId": versions[1]["VersionId"]},
        )
        print("Previous version uploaded as a new version")
