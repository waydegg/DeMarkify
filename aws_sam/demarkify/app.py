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

import torch
import torch.nn.functional as F
from torchvision import models, transforms

from requests_html import HTMLSession
import base64
from torchvision.utils import save_image



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

# get imgbb api upload key (fix this so its hidden?)
IMGBB_KEY = os.environ.get("IMGBB_KEY")
logger.info(f"Imgbb key is {IMGBB_KEY}")

# torch image preprocessing
preprocess = transforms.Compose([
    transforms.Resize((192,192)),
    transforms.ToTensor()
])

def load_model():
    logger.info('Loading model from S3')    
    obj = s3.get_object(Bucket=MODEL_BUCKET, Key=MODEL_KEY)
    bytestream = io.BytesIO(obj['Body'].read())
    tar = tarfile.open(fileobj=bytestream, mode="r:gz")
    member = tar.getmembers()[0]
    print("Model file is: ", member.name)
    f = tar.extractfile(member)
    print("Loading PyTorch model")
    model = torch.jit.load(io.BytesIO(f.read()), map_location=torch.device('cpu')).eval()
    return model

model = load_model()

def predict(input_object, model, local_repo):
    logger.info("Predicting image...")
    predict_values = model(input_object)
    predict_values = predict_values.squeeze()
    logger.info("Saving Image to Filesystem...")
    image_path = f"{local_repo}/gen_image.png"
    save_image(predict_values, image_path)
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
    # upload to imgbb
    session = HTMLSession()
    upload_form = {
        "image": encoded_image
    }
    r = session.post(
        f"https://api.imgbb.com/1/upload?key={IMGBB_KEY}",
        data=upload_form)
    return r.json()

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

    print("Creating tmp directory")
    local_repo = os.path.join(os.path.sep, "tmp", os.path.basename(os.getcwd()))
    if not os.path.exists(local_repo):
        os.makedirs(local_repo)
    
    print("Getting input object")
    input_object = input_fn(event['body'])
    print("Calling prediction")
    response = predict(input_object, model, local_repo)
    print("Returning response")
    
    # return{
    #     "statusCode":200,
    #     "body": json.dumps("TEST OUTPUT")
    # }
    
    
    return{
        "statusCode": 200,
        "body": json.dumps(response)
    }