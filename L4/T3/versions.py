# Run: python L4/T3/versions.py my-bucket-name --status
#      python L4/T3/versions.py my-bucket-name file.txt --list
#      python L4/T3/versions.py my-bucket-name file.txt --restore

import argparse

import boto3
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("bucket_name")
parser.add_argument("file_name", nargs="?")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--status", action="store_true", help="show if bucket versioning is enabled")
group.add_argument("--list", action="store_true", help="show file versions count and dates")
group.add_argument("--restore", action="store_true", help="upload the previous version as a new version")
args = parser.parse_args()

s3 = boto3.client("s3")

if args.status:
    status = s3.get_bucket_versioning(Bucket=args.bucket_name).get("Status", "Disabled")
    print(f"Versioning: {status}")
else:
    if not args.file_name:
        parser.error("file_name is required for --list and --restore")
    response = s3.list_object_versions(Bucket=args.bucket_name, Prefix=args.file_name)
    versions = [v for v in response.get("Versions", []) if v["Key"] == args.file_name]

    if args.list:
        print(f"Versions: {len(versions)}")
        for v in versions:
            print(f"{v['VersionId']} {v['LastModified']}")
    else:
        if len(versions) < 2:
            parser.error("file has no previous version")
        previous = versions[1]
        s3.copy_object(
            Bucket=args.bucket_name,
            Key=args.file_name,
            CopySource={"Bucket": args.bucket_name, "Key": args.file_name, "VersionId": previous["VersionId"]},
        )
        print(f"Restored version {previous['VersionId']} as new version")
