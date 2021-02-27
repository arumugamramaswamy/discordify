"""A module to help create reply messages using the output of a function"""
import typing as T
import numpy as np
import io
from PIL import Image
from discord import File

def _is_image(canditate_img):

    if isinstance(canditate_img, np.ndarray):

        if canditate_img.dtype == np.uint8:
            if 4 > len(canditate_img) > 1:
                return True
        elif canditate_img.dtype == np.float32:
            if canditate_img.max() <= 1 and canditate_img.min()>=0:
                return True
    
    return False

def create_msg(content: T.Any=None, images: T.List[np.array] = None, files: str = None) -> T.Dict[str, T.Any]:
    """Create a message using the input content, images and files"""
    msg_files = []
    if images is not None:
        for image in images:
            img = Image.fromarray(image)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            img_bytes = buf.getvalue()
            msg_files.append(File(img_bytes))

    for file in files:
        msg_files.append(File(file))

    return {"content": content, "files": msg_files}

def parse_reply(reply: T.Union[T.Tuple, T.Any]):

    parsed_reply = []
    files = []
    images = []
 
    if not isinstance(reply, tuple):
        reply = (reply,)

    for obj in reply:

        if _is_image(obj):
            images.append(obj)
            parsed_reply.append(f"image {len(images)}")

        else:
            parsed_reply.append(repr(obj))
        
    parsed_reply = ",".join(parsed_reply)
            
    return dict(content=parsed_reply, files=files, images=images)