# Run: python L3/T4/organize_by_extension.py my-bucket-name -o

import argparse
from collections import Counter

import boto3
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("bucket_name")
parser.add_argument("-o", "--organize", action="store_true")
args = parser.parse_args()

s3 = boto3.client("s3")
counts = Counter()

if args.organize:
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=args.bucket_name):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if "/" in key or "." not in key:  # already in a folder, or no extension
                continue
            extension = key.rsplit(".", 1)[1].lower()
            s3.copy_object(Bucket=args.bucket_name, Key=f"{extension}/{key}",
                           CopySource={"Bucket": args.bucket_name, "Key": key})
            s3.delete_object(Bucket=args.bucket_name, Key=key)
            counts[extension] += 1

for extension, count in counts.items():
    print(f"{extension} - {count}")
