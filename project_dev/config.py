from pathlib import Path
from fastai.vision import *
### PATHING
# Main
PATH = Path("data")
CLEAN = PATH/'clean'
MARKED = PATH/'marked'
IMG_GEN = PATH/'image_gen'
TEST = PATH/'test'

# Subset
SUB = PATH/'subset'
CLEAN_SUB = SUB/'clean_sub'
MARKED_SUB = SUB/'marked_sub'
IMG_GEN_SUB = SUB/'image_gen_sub'

### MODELING
proj_id = 'imagenet_all_new' # CHANGE WHEN RE-TRAINING MODELS
gen_name = proj_id + '_gen'
pre_gen_name = gen_name + '_0'
crit_name = proj_id + '_crit'

# Hyperparams
nf_factor = 1.5
pct_start = 1e-8
random_seed=42

# Model
arch = models.resnet34


### IMAGE TRANSFORM
prob = 1
brightness_range = (0.25,0.75)
contrast_range = (0.75,1.25)
jitter_mag = (0.005,0.01)
max_warp = (0.3)
rotate_range = (0,25)
zoom_range = (1., 1.125)
img_size = (128,512)
x_pct = (0.25,0.75)
y_pct = (0.25,0.75)

# Transforms
trn_tfms = [
#     brightness(change=brightness_range, use_on_y=False),
#     contrast(scale=contrast_range, use_on_y=False),
#     crop_pad(size=img_size, row_pct=x_pct, col_pct=y_pct, use_on_y=False), # Random Expand 
#     flip_lr(p=prob, use_on_y=False), # Flips Image
#     jitter(magnitude=jitter_mag, use_on_y=False),
#     perspective_warp(magnitude=(-max_warp,max_warp), use_on_y=False),
    rand_zoom(scale=zoom_range),
#     rotate(degrees=rotate_range, use_on_y=False)
]

val_tfms = [crop_pad(use_on_y=False)] 
tfms = (trn_tfms, val_tfms)

### AWS
# S3
bucket = "demarkify-models"
s3_fp = lambda export_fn: f"{bucket}/demarkify/{export_fn}.tar.gz"
