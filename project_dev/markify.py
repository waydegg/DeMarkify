import os
import numpy as np
import string, time, random
from pathlib import Path
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageFile
from tqdm import tqdm, tqdm_notebook
ImageFile.LOAD_TRUNCATED_IMAGES = True
import pdb


def draw_random_text(img, blank_img):  
    """
    Draws a single, random enlarged string of text centered on an image.

    Parameters:
        img: A PIL image object used as the background (the original image).
        blank_img: A "trasparent" PIL image object used as the foreground (the watermark).
    """
    # Configuration
    w,h = img.size
    draw_blank = ImageDraw.Draw(blank_img)    
    
    # Font properties
    font_list = ["dejavu", "abyssinica", "tibetan-machine", "liberation2", "padauk", "Sahadeva", "ubuntu",
                 "fonts-gujr-extra", "fonts-beng-extra", "fonts-deva-extra", "malayalam", "freefont", "ttf-khmeros-core",
                 "pagul", "tlwg", "lohit-telugu", "lohit-devanagari", "Nakula", "Sarai", "lao", "Gargi",
                 "liberation"]
    text_sz = np.random.randint(50,150)
    text_len = np.random.randint(4,16)
    text_opct = np.random.randint(50,125)
    text_string = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=text_len))
    colors = {"dark":np.random.randint(0,50), "light":np.random.randint(200,256)}
    tc,oc = np.random.choice(list(colors.values()), size=2, replace=False)

    # Select Font
    FONTS_PATH = Path("/usr/share/fonts/truetype/")
    FONT_PATH = Path(FONTS_PATH/np.random.choice(font_list))
    SUBFONT_PATH = str(Path(FONT_PATH/np.random.choice(os.listdir(FONT_PATH))))
    fnt = ImageFont.truetype(SUBFONT_PATH,text_sz)
    fw,fh = fnt.getsize(text_string)

    # Draw text
    thickness = np.random.randint(1,5)
    
    draw_blank.text((w/2-fw/2 - thickness,h/2-fh/2 - thickness), text_string, font=fnt, fill=(oc,oc,oc,text_opct))
    draw_blank.text((w/2-fw/2 + thickness,h/2-fh/2 - thickness), text_string, font=fnt, fill=(oc,oc,oc,text_opct))
    draw_blank.text((w/2-fw/2 - thickness,h/2-fh/2 + thickness), text_string, font=fnt, fill=(oc,oc,oc,text_opct))
    draw_blank.text((w/2-fw/2 + thickness,h/2-fh/2 + thickness), text_string, font=fnt, fill=(oc,oc,oc,text_opct))
    
    draw_blank.text((w/2-fw/2,h/2-fh/2), text_string, font=fnt, align="center", fill=(tc,tc,tc,text_opct))
    
    # Random rotation
    degree = np.random.randint(-15,15)
    blank_img = blank_img.rotate(degree)
    
    out = Image.alpha_composite(img, blank_img)

    return out

def draw_grid(img, blank_img):
    """
    Draws a grid pattern on an image.

    Parameters:
        img: A PIL image object used as the background (the original image).
        blank_img: A "trasparent" PIL image object used as the foreground (the watermark).
    """
    # Configuration
    w,h = img.size
    draw_blank = ImageDraw.Draw(blank_img)
    
    # Coordinates
    line_spacing = np.random.randint(50,100)
    
    x_coords = range(0, w, line_spacing)
    x1 = zip(x_coords,[0]*len(x_coords))
    x2 = zip(x_coords,[h]*len(x_coords))
    h_points = zip(x1,x2)
    
    y_coords = range(0, h, line_spacing)
    y1 = zip([0]*len(y_coords), y_coords)
    y2 = zip([w]*len(y_coords), y_coords)
    w_points = zip(y1,y2)
    
    
    # Color properties
    lc = np.random.randint(200,256)
    lo = np.random.randint(50,125)
    
    
    # Draw lines
    line_thickness = np.random.randint(1,5)
    
    for points in h_points:
        draw_blank.line(points, fill=(lc,lc,lc,lo), width=line_thickness)
        
    for points in w_points:
        draw_blank.line(points, fill=(lc,lc,lc,lo), width=line_thickness)

    # Rotate image
    degree = np.random.randint(-45,45)
    blank_img = blank_img.rotate(degree)
    
    out = Image.alpha_composite(img, blank_img)
    return out

def draw_center_x(img, blank_img):
    """
    Draws an "X" pattern on an image, a common/basic watermark seen in the real world.

    Parameters:
        img: A PIL image object used as the background (the original image).
        blank_img: A "trasparent" PIL image object used as the foreground (the watermark).
    """
    # Configuration
    w,h = img.size
    draw_blank = ImageDraw.Draw(blank_img)
    
    coords = [((0,0),(w,h)),((0,h),(w,0))]
    lc = np.random.randint(200,256)
    lo = np.random.randint(50,125)
    line_thickness = np.random.randint(1,5)
    
    # Draw lines
    for coord in coords:
        draw_blank.line(coord, fill=(lc,lc,lc,lo), width=5)
    
    
    out = Image.alpha_composite(img, blank_img)
    return out

def draw_repeating_text(img, blank_img):
    """
    Repeats text across an image.

    Parameters:
        img: A PIL image object used as the background (the original image).
        blank_img: A "trasparent" PIL image object used as the foreground (the watermark).
    """
    
    # Configuration
    w,h = img.size
    draw_blank = ImageDraw.Draw(blank_img)
    
    
    # Font properties
    font_list = ["dejavu", "abyssinica", "tibetan-machine", "liberation2", "padauk", "Sahadeva", "ubuntu",
                 "fonts-gujr-extra", "fonts-beng-extra", "fonts-deva-extra", "malayalam", "freefont", "ttf-khmeros-core",
                 "pagul", "tlwg", "lohit-telugu", "lohit-devanagari", "Nakula", "Sarai", "lao", "Gargi",
                 "liberation"]
    text_sz = np.random.randint(15,50)
    text_len = np.random.randint(4,10)
    text_opct = np.random.randint(50,125)
    text_string = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=text_len))
    colors = {"dark":np.random.randint(0,50), "light":np.random.randint(200,256)}
    tc,oc = np.random.choice(list(colors.values()), size=2, replace=False)

    
    # Select Font
    FONTS_PATH = Path("/usr/share/fonts/truetype/")
    FONT_PATH = Path(FONTS_PATH/np.random.choice(font_list))
    SUBFONT_PATH = str(Path(FONT_PATH/np.random.choice(os.listdir(FONT_PATH))))
    fnt = ImageFont.truetype(SUBFONT_PATH,text_sz)
    fw,fh = fnt.getsize(text_string)
    
    
    # Coordinates
    text_spacing = fw + np.random.randint(50,100)
    x_coords = range(0, w, text_spacing)
    y_coords = range(0, h, text_spacing)
    

    # Draw text
    for x in x_coords:
        for y in y_coords:
            draw_blank.text((x,y), text_string, font=fnt, align="center", fill=(tc,tc,tc,text_opct))
        
        
    # Rotate image
    degree = np.random.randint(-45,45)
    blank_img = blank_img.rotate(degree)
    
    
    out = Image.alpha_composite(img, blank_img)
    return out

def markify(clean_path, marked_path):
    """
    Driver function for creating watermarked images.

    Parameters:
        clean_path: directory of non-marked images
        marked_path: directory to save marked images
    """
    os.system(f"rm -rf {marked_path}")
    marked_path.mkdir(exist_ok=True)    

    for i, img_path in enumerate(tqdm_notebook(clean_path.ls(), desc="Marking")):
        img_path = str(img_path)
        # Load image elements
        img = PIL.Image.open(img_path).convert("RGBA")
        blank_img = Image.new('RGBA', img.size, (255,255,255,0))

        # Set which Markify functions to use
        filter_groups = {
            "random_text":draw_random_text,
            "center_x":draw_center_x,
            "grid":draw_grid,
            "repeating_text":draw_repeating_text
        }

        group = np.random.choice(
            list(filter_groups.values()), 
            size=np.random.randint(1,len(filter_groups)+1), 
            replace=False)

        for item in group:
            marked_img = item(img, blank_img)

        # Save image
        file_name = img_path.split('/')[-1]
        marked_img.save(marked_path/file_name)
