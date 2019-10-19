try:
    import unzip_requirements
except ImportError:
    pass

import os
import io
import json
import tarfile
import glob
import time
import logging

import boto3
import requests
import PIL

import pdb

import torch
import torch.nn.functional as F
from torchvision import models, transforms


# load s3 client
s3 = boto3.client('s3')

# load logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# get bucket name from ENV variable
MODEL_BUCKET = os.environ.get('MODEL_BUCKET')
logger.info(f"Model Bucket is {MODEL_BUCKET}")

# get bucket prefix from ENV variable
MODEL_KEY = os.environ.get('MODEL_KEY')
logger.info(f"Model Prefix is {MODEL_KEY}")

# torch image preprocessing
preprocess = transforms.Compose([
    transforms.Resize((300,300)),
    transforms.ToTensor()
])

def load_model():
    logger.info('Loading model from S3')
    obj = s3.get_object(Bucket=MODEL_BUCKET, Key=MODEL_KEY)
    bytestream = io.BytesIO(obj['Body'].read())
    tar = tarfile.open(fileobj=bytestream, mode="r:gz")
    for member in tar.getmembers():
        if member.name.endswith(".pkl"):
            print("Model file is: ", member.name)
            f = tar.extractfile(member)
            print("Loading PyTorch model")
            model = torch.jit.load(io.BytesIO(f.read()), map_location=torch.device('cpu')).eval()
    return model

model = load_model()

def predict(input_object, model):
    logger.info("Calling predictionn model")
    start_time = time.time()
    predict_values = model(input_object)
    predict_values = predict_values.squeeze()
    logger.info("--- Inference timne: %s seconds ---" % (time.time() - start_time))
    return "SUCCESSFULLY MADE PREDICTION"

def input_fn(request_body):
    logger.info("Getting input URL to a image Tensor object")
    if isinstance(request_body, str):
        request_body = json.loads(request_body)
    img_request = requests.get(request_body['url'], stream=True)
    img = PIL.Image.open(io.BytesIO(img_request.content))
    img_tensor = preprocess(img)
    img_tensor = img_tensor.unsqueeze(0)
    return img_tensor

def lambda_handler(event, context):
    print("Starting event")
    logger.info(event)
    print("Getting input object")
    input_object = input_fn(event['body'])
    print("Calling prediction")
    response = predict(input_object, model)
    print("Returning response")
    return{
        "statusCode": 200,
        "body": json.dumps(response)
    }