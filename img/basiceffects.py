from io import BytesIO
from PIL import Image
import PIL.ImageOps
import numpy as np

def invert(img):
    arr = np.array(img)

    arr = 255 - arr
    arr = np.clip(arr, 0, 255)

    return Image.fromarray(arr)
