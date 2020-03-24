from config import *
import gc
from tqdm import tqdm_notebook
import pdb
from fastai2.basics import *
from fastai2.callback.all import *
from fastai2.vision.all import *
from fastai2.vision.gan import *
from PIL import ImageDraw, ImageFont, ImageFile
# If true, ignores metadata of large, compressed images
ImageFile.LOAD_TRUNCATED_IMAGES = False


def get_dls(bs, size, keep_pct):
    "Builds a DataLoader for a Generator Learner"

    def get_image_files_subset(fp):
        "Gets a random subset of files (might already be v2 functionality)"
        files = get_image_files(fp)
        n_subset = int(len(files)*keep_pct)
        return L(list(np.random.choice(files, size=n_subset, replace=False)))

    dblock = DataBlock(blocks=(ImageBlock, ImageBlock),
                       get_items=get_image_files_subset,
                       get_y=lambda x: CLEAN/x.name,
                       splitter=RandomSplitter(),
                       item_tfms=[Resize(size)],
                       batch_tfms=[*aug_transforms(), Normalize.from_stats(*imagenet_stats)])

    dls = dblock.dataloaders(MARKED, bs=bs, path=DATA)
    dls.c = 3
    return dls


def create_gen_learner(dls_gen, arch, loss_gen, y_range):
    "Builds a Generator Learner"
    return unet_learner(dls_gen, arch, loss_func=loss_gen,
                        config=unet_config(blur=True, norm_type=NormType.Weight,
                                           self_attention=True, y_range=y_range))


def save_preds(learn_gen, dl):
    "Saves predicted images per batch from the given DataLoader"
    if GEN.exists():
        shutil.rmtree(GEN)
    GEN.mkdir(exist_ok=True)

    # batch-wise preds
    items = dl.items
    for batch_index, batch in tqdm_notebook(enumerate(dl), total=len(dl), desc="batches"):

        # get predictions
        torch.cuda.empty_cache()
        with torch.no_grad():
            preds = learn_gen.model(batch[0])

        # save to file
        for item_index, pred in enumerate(preds):
            dec = dl.after_batch.decode(
                (TensorImage(pred.to('cpu')[None]),))[0][0]
            arr = dec.numpy().transpose(1, 2, 0)
            index = batch_index * dl.bs + item_index
            Image.fromarray(np.uint8(arr), mode='RGB').save(
                GEN/items[index].name)


def get_crit_dls(bs, size):
    "Builds a DataLoader for a Critic Learner"
    crit_dblock = DataBlock(blocks=(ImageBlock, CategoryBlock),
                            get_items=partial(get_image_files, folders=[
                                              name_gen, 'clean']),
                            get_y=parent_label,
                            splitter=RandomSplitter(0.1, seed=42),
                            item_tfms=Resize(size),
                            batch_tfms=[Normalize.from_stats(*imagenet_stats)])
    return crit_dblock.dataloaders(DATA, bs=bs, path=DATA)


def create_critic_learner(dls, metrics, loss_critic):
    "Builds a Critic Learner"
    return Learner(dls, gan_critic(), metrics=metrics, loss_func=loss_critic)
