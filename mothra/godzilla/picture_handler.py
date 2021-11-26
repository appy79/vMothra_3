import os
from PIL import Image

from flask import url_for, current_app


def add_challenge_pic(pic_upload, fname):

    filename = pic_upload.filename
    ext_type = filename.split(".")[-1]
    storage_filename = str(fname) + "." + ext_type

    filepath = os.path.join(
        current_app.root_path, "static/challenge_pics", storage_filename
    )

    pic = Image.open(pic_upload)
    pic.save(filepath)

    return storage_filename
