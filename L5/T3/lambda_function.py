import boto3

s3_client = boto3.client("s3")


def lambda_handler(event, _):
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        if "/" in key or "." not in key:
            continue

        extension = key.rsplit(".", 1)[1].lower()
        s3_client.copy_object(
            Bucket=bucket,
            Key=f"{extension}/{key}",
            CopySource={"Bucket": bucket, "Key": key},
        )
        s3_client.delete_object(Bucket=bucket, Key=key)
        print(f"Moved {key} to {extension}/{key}")

    return {"statusCode": 200}
