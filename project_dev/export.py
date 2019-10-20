import boto3
from config import *
import torch

def s3_upload(trace_input, model, export_fn):
    
    print("1. Convert Fastai learner to Torchscript model")
    jit_model = torch.jit.trace(model.model.float(), trace_input)
    output_path = str(PATH/export_fn)
    torch.jit.save(jit_model, output_path)

    print("2. Package to tar file")
    tar_file = str(PATH/"models"/f"{export_fn}.tar.gz")
    with tarfile.open(tar_file, 'w:gz') as f:
        f.add(output_path, arcname=export_fn)

    print("3. Upload to s3")
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(tar_file, bucket, s3_fp(export_fn))

    print(f"--- {export_fn} uploaded to s3 ---")