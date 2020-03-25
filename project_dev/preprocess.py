from config import *
import pdb
from fastai2.basics import *
from fastai2.vision.all import *
from PIL import ImageDraw, ImageFont, ImageFile
# if True, ignores metadata of large, compressed images
ImageFile.LOAD_TRUNCATED_IMAGES = True


def create_clean_image(clean_fp, img_fp):
    img = Image.open(img_fp).resize_max(max_h=1080, max_w=1080)
    fn = img_fp.name
    img.save(clean_fp/fn)


class Markr:
    def __init__(self, marked_path, fonts, save=True):
        self.MARKED = marked_path
        self.fonts = fonts
        self.failed_images = L()
        self.save = save

    def __call__(self, fn):
        if(fn in self.failed_images):
            self.failed_images.remove(fn)

        try:
            img = load_image(fn, mode="RGBA")
            blank_img = Image.new('RGBA', img.size, (255, 255, 255, 0))

            marked_img = self.draw_repeating_text(img, blank_img)
            # marked_img = self.draw_center_text(img, blank_img)
            # marked_img = self.draw_grid(img, blank_img)
            # marked_img = self.draw_center_x(img, blank_img)

            if self.save:
                marked_fn = fn.parts[-1]
                marked_img.save(self.MARKED/marked_fn)
            else:
                return marked_img
        except Exception as e:
            print(f"Failed on img {fn}:\n {e}")
            self.failed_images.append(fn)

    def draw_repeating_text(self, img, blank_img):
        """
        Repeats text across an image.

        Parameters:
            img: A PIL image object used as the background (the original image).
            blank_img: A "trasparent" PIL image object used as the foreground (the watermark).
        """
        # Configuration
        w, h = img.size
        draw_blank = ImageDraw.Draw(blank_img)

        # Font properties
        text_sz = np.random.randint(15, 50)
        text_len = np.random.randint(4, 10)
        text_opct = np.random.randint(50, 125)
        text_string = ''.join(random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=text_len))
        colors = {"dark": np.random.randint(
            0, 50), "light": np.random.randint(200, 256)}
        tc, oc = np.random.choice(list(colors.values()), size=2, replace=False)

        # Select Font
        font_path = str(np.random.choice(self.fonts))
        font = ImageFont.truetype(font_path, text_sz)
        fw, fh = font.getsize(text_string)

        # Coordinates
        text_spacing = fw + np.random.randint(50, 100)
        x_coords = range(0, w, text_spacing)
        y_coords = range(0, h, text_spacing)

        # Draw text
        for x in x_coords:
            for y in y_coords:
                draw_blank.text((x, y), text_string, font=font,
                                align="center", fill=(tc, tc, tc, text_opct))

        # Rotate image
        degree = np.random.randint(-45, 45)
        blank_img = blank_img.rotate(degree)

        out = Image.alpha_composite(img, blank_img)
        return out

    def draw_center_text(self, img, blank_img):
        """
        Draws a single, random enlarged string of text centered on an image.

        Parameters:
            img: A PIL image object used as the background (the original image).
            blank_img: A "trasparent" PIL image object used as the foreground (the watermark).
        """
        # Configuration
        w, h = img.size
        draw_blank = ImageDraw.Draw(blank_img)

        # Font properties
        text_sz = np.random.randint(50, 150)
        text_len = np.random.randint(4, 16)
        text_opct = np.random.randint(50, 125)
        text_string = ''.join(random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=text_len))
        colors = {"dark": np.random.randint(
            0, 50), "light": np.random.randint(200, 256)}
        tc, oc = np.random.choice(list(colors.values()), size=2, replace=False)

        # Select Font
        font_path = str(np.random.choice(self.fonts))
        font = ImageFont.truetype(font_path, text_sz)
        fw, fh = font.getsize(text_string)

        # Draw text
        thickness = np.random.randint(1, 5)

        draw_blank.text((w/2-fw/2 - thickness, h/2-fh/2 - thickness),
                        text_string, font=font, fill=(oc, oc, oc, text_opct))
        draw_blank.text((w/2-fw/2 + thickness, h/2-fh/2 - thickness),
                        text_string, font=font, fill=(oc, oc, oc, text_opct))
        draw_blank.text((w/2-fw/2 - thickness, h/2-fh/2 + thickness),
                        text_string, font=font, fill=(oc, oc, oc, text_opct))
        draw_blank.text((w/2-fw/2 + thickness, h/2-fh/2 + thickness),
                        text_string, font=font, fill=(oc, oc, oc, text_opct))

        draw_blank.text((w/2-fw/2, h/2-fh/2), text_string, font=font,
                        align="center", fill=(tc, tc, tc, text_opct))

        # Random rotation
        degree = np.random.randint(-15, 15)
        blank_img = blank_img.rotate(degree)

        out = Image.alpha_composite(img, blank_img)
        return out

    def draw_grid(self, img, blank_img):
        """
        Draws a grid pattern on an image.

        Parameters:
            img: A PIL image object used as the background (the original image).
            blank_img: A "trasparent" PIL image object used as the foreground (the watermark).
        """
        # Configuration
        w, h = img.size
        draw_blank = ImageDraw.Draw(blank_img)

        # Coordinates
        line_spacing = np.random.randint(50, 100)

        x_coords = range(0, w, line_spacing)
        x1 = zip(x_coords, [0]*len(x_coords))
        x2 = zip(x_coords, [h]*len(x_coords))
        h_points = zip(x1, x2)

        y_coords = range(0, h, line_spacing)
        y1 = zip([0]*len(y_coords), y_coords)
        y2 = zip([w]*len(y_coords), y_coords)
        w_points = zip(y1, y2)

        # Color properties
        lc = np.random.randint(200, 256)
        lo = np.random.randint(50, 125)

        # Draw lines
        line_thickness = np.random.randint(1, 5)

        for points in h_points:
            draw_blank.line(points, fill=(lc, lc, lc, lo),
                            width=line_thickness)

        for points in w_points:
            draw_blank.line(points, fill=(lc, lc, lc, lo),
                            width=line_thickness)

        # Rotate image
        degree = np.random.randint(-45, 45)
        blank_img = blank_img.rotate(degree)

        out = Image.alpha_composite(img, blank_img)
        return out

    def draw_center_x(self, img, blank_img):
        """
        Draws an "X" pattern on an image, a common/basic watermark seen in the real world.

        Parameters:
            img: A PIL image object used as the background (the original image).
            blank_img: A "trasparent" PIL image object used as the foreground (the watermark).
        """
        # Configuration
        w, h = img.size
        draw_blank = ImageDraw.Draw(blank_img)

        coords = [((0, 0), (w, h)), ((0, h), (w, 0))]
        lc = np.random.randint(200, 256)
        lo = np.random.randint(50, 125)
        line_thickness = np.random.randint(1, 5)

        # Draw lines
        for coord in coords:
            draw_blank.line(coord, fill=(lc, lc, lc, lo), width=5)

        out = Image.alpha_composite(img, blank_img)
        return out
