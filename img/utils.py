from io import BytesIO
from PIL import Image
import numpy as np

def arr_to_bytesIO(arr):
    """ Converts a numpy array to a BytesIO object.
    """
    f = BytesIO()
    Image.fromarray(arr.astype(np.uint8)).save(f, format="PNG")
    f.seek(0)
    return f

async def images_from_msg(message):
    """ Returns a list of images from a message.
    """
    images = []
    for attachment in message.attachments:
        img_bytes = await attachment.read()
        img = Image.open(BytesIO(img_bytes))
        images.append(img.convert("RGB"))
    return images
