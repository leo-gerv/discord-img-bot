from io import BytesIO
from PIL import Image
import numpy as np

def arr_to_bytesIO(arr):
    """ Converts a numpy array to a BytesIO object.
    """
    with BytesIO() as f:
        Image.fromarray(arr).save(f, format="PNG")
        f.seek(0)
        return f
