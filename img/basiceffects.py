from io import BytesIO
from PIL import Image
import PIL.ImageOps

def invert(file_bytes):
    img = Image.open(BytesIO(file_bytes))
    inverted_img = PIL.ImageOps.invert(img)
    with BytesIO() as f:
        inverted_img.save(f, format="PNG")
        f.seek(0)
        return f.read()
