import numpy as np
from PIL import Image
from io import BytesIO

def compression_anomaly_score(img: Image.Image):
    qualities = [95, 80, 60]
    arrays = []

    for q in qualities:
        buf = BytesIO()
        img.save(buf, "JPEG", quality=q)
        buf.seek(0)
        arrays.append(np.array(Image.open(buf).convert("L")).astype(float))

    stacked = np.stack(arrays)
    score = stacked.std(axis=0).mean() / 255.0
    return float(score)
