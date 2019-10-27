import boto3
from config import *

def get_credentials():

    s3 = boto3.recource("s3")
    s3.meta.client.download_file(bucket, 'OBJECT_NAME', 'larger_input.pkl')