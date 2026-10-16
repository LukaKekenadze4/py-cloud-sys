# Run: python L3/T2/delete_file.py my-bucket-name file.txt -del

import argparse

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("bucket_name")
parser.add_argument("key", help="File name (Key) in the bucket")
parser.add_argument("-del", "--delete", action="store_true", help="Delete the file")
args = parser.parse_args()

s3 = boto3.client("s3")

if args.delete:
    try:
        s3.head_object(Bucket=args.bucket_name, Key=args.key)
    except ClientError:
        print("File does not exist")
    else:
        s3.delete_object(Bucket=args.bucket_name, Key=args.key)
        print("File deleted")
