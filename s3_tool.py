# Run: poetry run s3-tool --help   (credentials are read from .env)

import argparse
import io
import json
import logging
from urllib.request import urlopen

import boto3
import puremagic
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

# .bmp, .jpg, .jpeg, .png, .webp, .mp4
ALLOWED_MIME_TYPES = {"image/bmp", "image/x-ms-bmp", "image/jpeg", "image/png",
                      "image/webp", "video/mp4"}


def init_client():
    client = boto3.client("s3")  # credentials come from the env variables
    client.list_buckets()  # fails if credentials are wrong
    return client


def list_buckets(client):
    return [b["Name"] for b in client.list_buckets()["Buckets"]]


def create_bucket(client, bucket_name):
    options = {"Bucket": bucket_name, "ObjectOwnership": "BucketOwnerPreferred"}
    region = client.meta.region_name
    if region != "us-east-1":
        options["CreateBucketConfiguration"] = {"LocationConstraint": region}
    client.create_bucket(**options)
    log.info("Bucket created")


def delete_bucket(client, bucket_name):
    client.delete_bucket(Bucket=bucket_name)
    log.info("Bucket deleted")


def bucket_exists(client, bucket_name):
    try:
        client.head_bucket(Bucket=bucket_name)
        return True
    except client.exceptions.ClientError:
        return False


def download_file_and_upload_to_s3(client, bucket_name, url, file_name, keep_local=False):
    with urlopen(url) as response:
        content = response.read()

    try:
        mime_type = puremagic.from_string(content, mime=True)
    except puremagic.PureError:
        mime_type = None
    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"Unsupported file type: {mime_type}. "
                         "Allowed: .bmp, .jpg, .jpeg, .png, .webp, .mp4")

    client.upload_fileobj(io.BytesIO(content), bucket_name, file_name,
                          ExtraArgs={"ContentType": mime_type})

    if keep_local:
        with open(file_name, "wb") as file:
            file.write(content)

    return f"https://{bucket_name}.s3.{client.meta.region_name}.amazonaws.com/{file_name}"


def set_object_access_policy(client, bucket_name, file_name):
    client.put_object_acl(ACL="public-read", Bucket=bucket_name, Key=file_name)
    log.info("ACL set")


def generate_public_read_policy(bucket_name):
    return json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*",
        }],
    })


def create_bucket_policy(client, bucket_name):
    client.delete_public_access_block(Bucket=bucket_name)  # otherwise AWS rejects public policies
    client.put_bucket_policy(Bucket=bucket_name, Policy=generate_public_read_policy(bucket_name))
    log.info("Bucket policy created")


def read_bucket_policy(client, bucket_name):
    return client.get_bucket_policy(Bucket=bucket_name)["Policy"]


def main():
    parser = argparse.ArgumentParser(description="Work with S3 buckets")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list")
    for name in ["create", "delete", "exists", "create-policy", "read-policy"]:
        sub.add_parser(name).add_argument("bucket_name")

    upload = sub.add_parser("upload")
    upload.add_argument("bucket_name")
    upload.add_argument("url")
    upload.add_argument("file_name")
    upload.add_argument("--keep-local", action="store_true")

    acl = sub.add_parser("set-acl")
    acl.add_argument("bucket_name")
    acl.add_argument("file_name")

    args = parser.parse_args()
    client = init_client()

    try:
        if args.command == "list":
            print("\n".join(list_buckets(client)))
        elif args.command == "create":
            create_bucket(client, args.bucket_name)
        elif args.command == "delete":
            delete_bucket(client, args.bucket_name)
        elif args.command == "exists":
            print("Bucket exists" if bucket_exists(client, args.bucket_name) else "Bucket does not exist")
        elif args.command == "create-policy":
            create_bucket_policy(client, args.bucket_name)
        elif args.command == "read-policy":
            print(read_bucket_policy(client, args.bucket_name))
        elif args.command == "upload":
            print(download_file_and_upload_to_s3(client, args.bucket_name, args.url,
                                                 args.file_name, args.keep_local))
        elif args.command == "set-acl":
            set_object_access_policy(client, args.bucket_name, args.file_name)
    except (client.exceptions.ClientError, ValueError) as e:
        log.error(e)


if __name__ == "__main__":
    main()
