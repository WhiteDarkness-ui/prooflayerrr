from PIL import Image, ImageChops, ImageEnhance
import numpy as np
from io import BytesIO

def run_ela(img: Image.Image, quality=90):
    buf = BytesIO()
    img.save(buf, "JPEG", quality=quality)
    buf.seek(0)

    recompressed = Image.open(buf).convert("RGB")
    diff = ImageChops.difference(img, recompressed)

    extrema = diff.getextrema()
    max_diff = max(e[1] for e in extrema) or 1
    scale = 255.0 / max_diff

    ela_img = ImageEnhance.Brightness(diff).enhance(scale)
    arr = np.array(ela_img).astype(float)
    score = arr.mean() / 255.0

    return ela_img, float(score)
