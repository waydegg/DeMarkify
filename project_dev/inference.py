from fastai.vision import *
from util import *
from config import *

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
