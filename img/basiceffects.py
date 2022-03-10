from io import BytesIO
from PIL import Image
import PIL.ImageOps

def invert(img):
    inverted_img = PIL.ImageOps.invert(img.convert("RGB"))
    return inverted_img
