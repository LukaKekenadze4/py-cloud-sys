# Run: python L3/T2/delete_file.py my-bucket-name file.txt -del

import argparse

import boto3
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("bucket_name")
parser.add_argument("key")
parser.add_argument("-del", "--delete", action="store_true")
args = parser.parse_args()

s3 = boto3.client("s3")

if args.delete:
    try:
        s3.head_object(Bucket=args.bucket_name, Key=args.key)  # delete_object succeeds even if the file is missing
    except s3.exceptions.ClientError:
        print("File does not exist")
    else:
        s3.delete_object(Bucket=args.bucket_name, Key=args.key)
        print("File deleted")
