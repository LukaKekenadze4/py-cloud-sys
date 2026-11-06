# Run: python L4/T1/upload.py path/to/file.txt my-bucket-name

import argparse
import os

import boto3
from dotenv import load_dotenv
import magic

load_dotenv()

parser = argparse.ArgumentParser(description="Upload a file to S3 into a folder based on its detected type")
parser.add_argument("file")
parser.add_argument("bucket")
args = parser.parse_args()

mime = magic.from_file(args.file, mime=True)
key = f"{mime.split('/')[0]}/{os.path.basename(args.file)}"

boto3.client("s3").upload_file(args.file, args.bucket, key, ExtraArgs={"ContentType": mime})
print(f"Uploaded to s3://{args.bucket}/{key}")
