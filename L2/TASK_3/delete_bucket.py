# Run: set -a; source .env; set +a; python L2/TASK_3/delete_bucket.py my-bucket-name

import argparse

import boto3
from botocore.exceptions import ClientError

parser = argparse.ArgumentParser()
parser.add_argument("bucket_name")
args = parser.parse_args()

s3 = boto3.client("s3")

try:
    s3.head_bucket(Bucket=args.bucket_name)
except ClientError as e:
    if e.response["Error"]["Code"] != "404":
        raise
    print("Bucket does not exist")
else:
    s3.delete_bucket(Bucket=args.bucket_name)
    print("Bucket deleted")
