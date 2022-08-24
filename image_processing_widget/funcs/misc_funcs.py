from pathlib import Path

import cv2 as cv
import numpy as np


def strtobool(val):
    """Convert a string representation of truth to true or false.

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    if isinstance(val, bool):
        return val

    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))


def imread(filename: Path, flags):
    data = np.fromfile(str(filename), dtype=np.uint8)
    return cv.imdecode(data, flags)


def imwrite(filename: Path, img):
    if img.ndim > 2:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    retval, buf = cv.imencode(ext=filename.suffix, img=img)
    if retval:
        buf.tofile(str(filename))
    else:
        raise Exception("Could not save file.")
