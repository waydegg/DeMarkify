from fastai.vision import *
from fastai.vision.gan import *
from tqdm import tqdm, tqdm_notebook
import shutil
from config import *

def get_data(bs,size, keep_pct, clean_path):
    """
    Returns a DataBunch object for a Fastai generator learner.

    Parameters:
        bs: Batch size
        size: Image size in pixels
        keep_pct: Percentage of images to keep from original folder
        clean_path: Path to un-watermarked images

    """
    src = (ImageImageList.from_folder(MARKED)
           .use_partial_data(sample_pct=keep_pct, seed=random_seed)
           .split_by_rand_pct(0.1, seed=random_seed))
    
    data = (src.label_from_func(lambda x: clean_path/x.name)
           .transform(tfms, size=size, tfm_y=True)
           .databunch(bs=bs).normalize(imagenet_stats, do_y=True))

    data.c = 3
    return data

def create_gen_learner(path):
    """
    Creates a Fastai GAN Learner.

    Parameters:
        path: Filepath to save learner object
    """
    return unet_learner(data_gen, arch, wd=wd, blur=True, norm_type=NormType.Weight,
                         self_attention=True, y_range=y_range, loss_func=loss_gen, path=path)

def save_preds(dl, learn_gen, path_gen):
    """
    Saves generated images to a folder.

    Parameters:
        dl: Fastai DataLoader object
        learner_gen: Fastai generator learner
        path_gen: Filepath to save generated images
    """
    i=0
    names = dl.dataset.items
    
    for b in dl:
        preds = learn_gen.pred_batch(batch=b, reconstruct=True)
        for o in preds:
            o.save(path_gen/names[i].name)
            i += 1

def get_crit_data(classes, bs, size, path):
    """
    Returns a DataBunch for a critic learner.

    Parameters:
        classes: A list of image folders to use 
        bs: Batch size
        size: Image size
        path: Filepath to folders in "classes"
    """
    src = ImageList.from_folder(path, include=classes).split_by_rand_pct(0.1, seed=random_seed)
    ll = src.label_from_folder(classes=classes)
    data = (ll.transform(get_transforms(max_zoom=2.), size=size)
           .databunch(bs=bs).normalize(imagenet_stats))
    data.c = 3
    return data

def create_critic_learner(data, metrics, path):
    """
    Creates a Fastai critic learner.

    Parameters:
        data: A databunch with critic data
        metrics: Accuracy metrics to use
        path: Filepath to class folders
    """
    return Learner(data, gan_critic(), metrics=metrics, loss_func=loss_critic, wd=wd, path=path)

def convert_to_png(img_path):
    """
    Converts images to png format.

    Parameters:
        img_path: Filepath of images to convert
    """
    # Remove non-convertable filetypes
    os.system(f"rm {img_path}/*.php")
    conversion_count = 0
    
    for img in os.listdir(img_path):
        if img[-4:] != ".png":
            tmp_img = PIL.Image.open(img_path/img).convert("RGBA")
            filename = img.split('.')[0]
            tmp_img.save(str(img_path/filename) + ".png")
            os.system(f"rm {img_path/img}")
            conversion_count += 1
            
            if conversion_count % 1000 == 0:
                print(f"Converted {conversion_count} images.")

def image_subset(size, clean_path, clean_sub_path):
    """
    Create a subset of images for testing.

    Parameters:
        size: Number of images
        clean_path: Filepath of images to take from
        clean_sub_path: Filepath to save subset
    """
    os.system(f"rm -rf {clean_sub_path}")
    clean_sub_path.mkdir(exist_ok=True)
    
    clean_list = os.listdir(clean_path)
    clean_index = np.random.randint(0,len(clean_list)-size)
    for i in tqdm_notebook(range(size), desc="Images"):
        img = clean_list[clean_index + i]
        shutil.copyfile(clean_path/img, clean_sub_path/img)

def demark_image(img, model):
    h,w = img.size
    if h%2 != 0:
        h -= 1
    if w%2 != 0:
        w -= 1
    model.data = get_data(1, (h,w), 1, config.CLEAN)
    output = model.predict(img)[0]
    return output