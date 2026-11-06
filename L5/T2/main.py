# Run: python L5/T2/main.py --inspire
#      python L5/T2/main.py --inspire "Aesop"
#      python L5/T2/main.py my-bucket-name --inspire "Aesop" -save

import argparse
import json

import boto3
import requests
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("bucket_name", nargs="?")
parser.add_argument("--inspire", nargs="?", const="", metavar="AUTHOR", required=True)
parser.add_argument("-save", action="store_true")
args = parser.parse_args()

if args.save and not args.bucket_name:
    parser.error("bucket_name is required with -save")

response = requests.get(
    "https://api.quotable.kurokeita.dev/api/quotes/random",
    params={"author": args.inspire} if args.inspire else {},
)
response.raise_for_status()
quote = response.json().get("quote")
if not quote:
    parser.error(f"no quotes found for author '{args.inspire}'")

print(f'"{quote["content"]}" - {quote["author"]["name"]}')

if args.save:
    key = f"{quote['id']}.json"
    boto3.client("s3").put_object(
        Bucket=args.bucket_name,
        Key=key,
        Body=json.dumps(quote, ensure_ascii=False),
        ContentType="application/json",
    )
    print(f"Saved to s3://{args.bucket_name}/{key}")
