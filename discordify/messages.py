"""A module to help create reply messages using the output of a function"""
import cv2
import logging
import typing as T
import PIL
import numpy as np
import io
from PIL import Image
from discord import File
logger = logging.getLogger(__name__)
def _is_image(canditate_img):

    if isinstance(canditate_img, np.ndarray):

        if canditate_img.dtype == np.uint8:
            if 4 > len(canditate_img.shape) > 1:
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
            # img = Image.fromarray(image)
            # logger.debug("PIL from numpy array %s", img)    
            # buf = io.BytesIO()
            # img.save(buf, format="PNG")
            # img_bytes = buf.getvalue()
            # cv2.imwrite("tmp.png", image)
            # _, img= cv2.imencode('.jpg',image)
            # logger.debug(img)
            # img_bytes = img.tobytes()
            # img_bytes = (b'--frame\r\n'
            #        b'Content-Type: image/jpeg\r\n\r\n' + img.tostring() + b'\r\n')
            # TODO: change this to not actaully write to file
            cv2.imwrite("/tmp/tmp.png", image)
            msg_files.append(File("/tmp/tmp.png"))

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

def np_array_from_png_bytes(png_bytes: bytes):

    image = Image.open(io.BytesIO(png_bytes))
    arr = np.array(image).astype(np.uint8)
    # import ipdb; ipdb.set_trace()
    return arr