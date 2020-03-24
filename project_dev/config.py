from fastai2.basics import *

DATA = Path("data")
RAW = Path(DATA/"flickr/in-the-wild-images")

CLEAN = Path(DATA/"clean")
CLEAN.mkdir(exist_ok=True)

MARKED = Path(DATA/"marked")
MARKED.mkdir(exist_ok=True)

name_gen = "image_gen"
GEN = DATA/name_gen


# # AWS
# # S3
# bucket = "demarkify-models"
# def s3_fp(export_fn): return f"{bucket}/{export_fn}.tar.gz"
# MODEL_BUCKET = "demarkify-models"
# MODEL_KEY = "serialized_baseline_01.tar.gz"
