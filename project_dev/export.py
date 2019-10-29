import boto3
from config import *
from inference import *
import torch
from database_util import *
import pdb

def s3_upload(trace_input, model, export_filename):
    "Uploads a Fastai model to S3"

    print("1. Convert Fastai learner to Torchscript model")
    jit_model = torch.jit.trace(model.model.float(), trace_input)
    output_path = str(PATH/export_filename)
    torch.jit.save(jit_model, output_path)

    print("2. Package to tar file")
    tar_file = str(PATH/"models"/f"{export_filename}.tar.gz")
    with tarfile.open(tar_file, 'w:gz') as f:
        f.add(output_path, arcname=export_filename)

    print("3. Upload to s3")
    s3_transfer(
        bucket_name="demarkify-models",
        file_name=tar_file,
        direction="upload")

    print(f"--- {export_filename} uploaded to s3 ---")

