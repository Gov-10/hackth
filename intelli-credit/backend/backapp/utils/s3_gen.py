import os
from dotenv import load_dotenv
import boto3
load_dotenv()
s3= boto3.client('s3', region_name=os.getenv("S3_REGION"), aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
bucket=os.getenv("S3_BUCKET_NAME")
def generate_url(key:str, method:str ):
    url=s3.generate_presigned_url(ClientMethod=method, Params={'Bucket': bucket, "Key": key, "ContentType": json}, ExpiresIn=600)
    return url
    
