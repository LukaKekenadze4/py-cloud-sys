# Run: python L4/T2/delete_old_versions.py my-bucket-name file1.txt file2.txt

import argparse
from datetime import datetime, timedelta, timezone

import boto3
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser(description="List versions of S3 objects and delete versions older than 6 months")
parser.add_argument("bucket")
parser.add_argument("keys", nargs="+")
args = parser.parse_args()

s3 = boto3.client("s3")
limit = datetime.now(timezone.utc) - timedelta(days=180)

for key in args.keys:
    versions = s3.list_object_versions(Bucket=args.bucket, Prefix=key).get("Versions", [])
    for v in versions:
        if v["Key"] != key:
            continue
        old = v["LastModified"] < limit
        print(f"{key} {v['VersionId']} {v['LastModified']} {'DELETE' if old else 'keep'}")
        if old:
            s3.delete_object(Bucket=args.bucket, Key=key, VersionId=v["VersionId"])
