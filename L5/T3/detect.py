# Run: python L5/T3/detect.py my-bucket-name path/to/image.jpg

import argparse
import json
import os

import boto3
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("bucket_name")
parser.add_argument("image")
args = parser.parse_args()

with open(args.image, "rb") as file:
    image = file.read()

result = boto3.client("rekognition").detect_labels(Image={"Bytes": image}, MaxLabels=10)
name = os.path.basename(args.image)

s3 = boto3.client("s3")
s3.put_object(Bucket=args.bucket_name, Key=name, Body=image)
s3.put_object(
    Bucket=args.bucket_name,
    Key=f"{name.rsplit('.', 1)[0]}.json",
    Body=json.dumps(result["Labels"], indent=2),
)
print(json.dumps(result["Labels"], indent=2))
