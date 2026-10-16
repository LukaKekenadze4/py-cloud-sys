# Run: python L3/T1/upload_small_file.py my-bucket-name path/to/file.txt

import argparse
import os

import boto3
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("bucket_name")
parser.add_argument("file_path")
args = parser.parse_args()

s3 = boto3.client("s3")
key = os.path.basename(args.file_path)

with open(args.file_path, "rb") as file:
    s3.put_object(Bucket=args.bucket_name, Key=key, Body=file)

print(f"Uploaded to s3://{args.bucket_name}/{key}")
