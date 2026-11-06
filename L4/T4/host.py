# Run: python L4/T4/host.py my-bucket-name

import argparse
import json

import boto3
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("bucket_name")
args = parser.parse_args()

s3 = boto3.client("s3")

s3.upload_file("L4/T4/index.html", args.bucket_name, "index.html", ExtraArgs={"ContentType": "text/html"})
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
