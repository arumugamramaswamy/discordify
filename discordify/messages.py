import numpy as np
import io
from PIL import Image
from discord import File
def create_msg(text=None, image: np.array = None, files=None):

    img = Image.fromarray(image)
    buf = io.BytesIO() 
    img.save(buf, format="PNG")
    img_bytes = buf.getvalue()

    msg_files = []
    msg_files.append(File(img_bytes))

    for file in files:
        msg_files.append(File(file))
    
    return {
        "text":text,
        "files": msg_files
    }