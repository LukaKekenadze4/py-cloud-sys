# Run: set -a; source .env; set +a; python L2/TASK_1/create_bucket.py my-bucket-name

import argparse

import boto3
from botocore.exceptions import ClientError

parser = argparse.ArgumentParser()
parser.add_argument("bucket_name")
args = parser.parse_args()

s3 = boto3.client("s3")

try:
    s3.head_bucket(Bucket=args.bucket_name)
    print("Bucket already exists")
except ClientError:
    region = s3.meta.region_name
    if region == "us-east-1":
        s3.create_bucket(Bucket=args.bucket_name)
    else:
        s3.create_bucket(
            Bucket=args.bucket_name,
            CreateBucketConfiguration={"LocationConstraint": region},
        )
    print("Bucket created")
