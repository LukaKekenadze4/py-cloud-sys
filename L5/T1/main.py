# Run: python L5/T1/main.py host my-bucket-name --source L5/T1/html_demo_site

import argparse
import json
import mimetypes
import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", required=True)
host = subparsers.add_parser("host")
host.add_argument("bucket_name")
host.add_argument("--source", required=True)
args = parser.parse_args()

s3 = boto3.client("s3")

try:
    s3.head_bucket(Bucket=args.bucket_name)
except ClientError:
    s3.create_bucket(Bucket=args.bucket_name)

for root, _, files in os.walk(args.source):
    for name in files:
        path = os.path.join(root, name)
        key = os.path.relpath(path, args.source)
        content_type = mimetypes.guess_type(path)[0] or "binary/octet-stream"
        s3.upload_file(path, args.bucket_name, key, ExtraArgs={"ContentType": content_type})

s3.put_bucket_website(
    Bucket=args.bucket_name,
    WebsiteConfiguration={"IndexDocument": {"Suffix": "index.html"}},
)
s3.delete_public_access_block(Bucket=args.bucket_name)
s3.put_bucket_policy(
    Bucket=args.bucket_name,
    Policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{args.bucket_name}/*",
        }],
    }),
)

print(f"http://{args.bucket_name}.s3-website-{s3.meta.region_name}.amazonaws.com")
