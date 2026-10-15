# Run: set -a; source .env; set +a; python L2/TASK_2/bucket_policy.py my-bucket-name

import argparse
import json

import boto3
from botocore.exceptions import ClientError

parser = argparse.ArgumentParser()
parser.add_argument("bucket_name")
args = parser.parse_args()

s3 = boto3.client("s3")
bucket = args.bucket_name

try:
    s3.get_bucket_policy(Bucket=bucket)
    print("Policy already exists")
except ClientError as e:
    if e.response["Error"]["Code"] != "NoSuchBucketPolicy":
        raise

    # By default Block Public Access rejects public policies, so turn it off first
    s3.put_public_access_block(
        Bucket=bucket,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": False,
            "IgnorePublicAcls": False,
            "BlockPublicPolicy": False,
            "RestrictPublicBuckets": False,
        },
    )

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": [
                    f"arn:aws:s3:::{bucket}/dev/*",
                    f"arn:aws:s3:::{bucket}/test/*",
                ],
            }
        ],
    }
    s3.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy))
    print("Policy created")
