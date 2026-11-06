# Run: python L5/T3/deploy.py my-bucket-name

import argparse
import io
import zipfile

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("bucket_name")
args = parser.parse_args()

s3 = boto3.client("s3")
lambda_client = boto3.client("lambda")
FUNCTION = "extension-router"

try:
    s3.head_bucket(Bucket=args.bucket_name)
except ClientError:
    s3.create_bucket(Bucket=args.bucket_name)

buffer = io.BytesIO()
with zipfile.ZipFile(buffer, "w") as archive:
    archive.write("L5/T3/lambda_function.py", "lambda_function.py")

role_arn = boto3.client("iam").get_role(RoleName="LabRole")["Role"]["Arn"]
function_arn = lambda_client.create_function(
    FunctionName=FUNCTION,
    Runtime="python3.12",
    Role=role_arn,
    Handler="lambda_function.lambda_handler",
    Code={"ZipFile": buffer.getvalue()},
)["FunctionArn"]
lambda_client.get_waiter("function_active_v2").wait(FunctionName=FUNCTION)

lambda_client.add_permission(
    FunctionName=FUNCTION,
    StatementId="s3-invoke",
    Action="lambda:InvokeFunction",
    Principal="s3.amazonaws.com",
    SourceArn=f"arn:aws:s3:::{args.bucket_name}",
)
s3.put_bucket_notification_configuration(
    Bucket=args.bucket_name,
    NotificationConfiguration={
        "LambdaFunctionConfigurations": [
            {"LambdaFunctionArn": function_arn, "Events": ["s3:ObjectCreated:*"]}
        ]
    },
)

print(f"Deployed {FUNCTION} on bucket {args.bucket_name}")
