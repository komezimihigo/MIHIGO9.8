import os

def make_s3_client():
    """Create an S3-compatible B2 client from environment variables; optional dependency."""
    try: import boto3
    except ImportError as e: raise RuntimeError('Install boto3 to enable B2 storage') from e
    key=os.getenv('B2_KEY_ID'); secret=os.getenv('B2_APPLICATION_KEY'); endpoint=os.getenv('B2_ENDPOINT'); region=os.getenv('B2_REGION','us-west-004')
    if not all([key,secret,endpoint]): raise RuntimeError('Set B2_KEY_ID, B2_APPLICATION_KEY and B2_ENDPOINT in environment/secrets')
    return boto3.client('s3',endpoint_url=endpoint,region_name=region,aws_access_key_id=key,aws_secret_access_key=secret)

def upload_file(path: str, key: str, bucket: str|None=None):
    bucket=bucket or os.getenv('B2_BUCKET_NAME')
    if not bucket: raise RuntimeError('Set B2_BUCKET_NAME')
    client=make_s3_client(); client.upload_file(path,bucket,key); return key
