from fastai.vision import *
from util import *
from config import *
import boto3

class markify_learner():
    def __init__(self, model_path, fn):
        self.model = load_learner(model_path, fn)
    
    def generate_image(self, img):
        h,w = img.size
        if h%2 != 0:
            h -= 1
        if w%2 != 0:
            w -= 1
    
        self.model.data = get_data(1, (h,w), 1, CLEAN)
        gen_img = self.model.predict(img)[0]
        return gen_img

def load_model(use_s3=True, saved_model=None):
    if use_s3:
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=MODEL_BUCKET, Key=MODEL_KEY)
        bytestream = io.BytesIO(obj['Body'].read())
        tar = tarfile.open(fileobj=bytestream, mode="r:gz")
    else:
        tar = tarfile.open(saved_model, mode="r:gz")
        
    member = tar.getmembers()[0]
    print("Model file is: ", member.name)
    f = tar.extractfile(member)
    print("Loading PyTorch model")
    model = torch.jit.load(io.BytesIO(f.read()), map_location=torch.device('cpu')).eval()
    return model

def predict(input_object, model):
    predict_values = model(input_object)
    return predict_values

def input_fn(request_body):
    if isinstance(request_body, str):
        request_body = json.loads(request_body)
    img_request = requests.get(request_body['url'], stream=True)
    img = PIL.Image.open(io.BytesIO(img_request.content))
    img_tensor = preprocess(img)
    img_tensor = img_tensor.unsqueeze(0)
    return img_tensor

def lambda_handler(event, context):    
    print("Starting event")
    print("Getting input object")
    input_object = input_fn(event['body'])
    
    print(input_object)
    time.sleep(10)
    
    print("Calling prediction")
    response = predict(input_object, model)
    print("Returning response")
    return{
        "statusCode": 200,
        "body": json.dumps(response)
    }