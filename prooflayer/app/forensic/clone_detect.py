import numpy as np
from PIL import Image

def detect_clone_regions(img: Image.Image, block=32, stride=16):
    gray = np.array(img.convert("L"))
    h, w = gray.shape
    blocks = {}

    for y in range(0, h - block, stride):
        for x in range(0, w - block, stride):
            patch = gray[y:y+block, x:x+block]
            key = hash(patch.tobytes())
            blocks.setdefault(key, []).append((x, y))

    dup_blocks = sum(len(v) for v in blocks.values() if len(v) > 1)
    total = max(1, len(blocks))
    score = dup_blocks / total

    mask = np.zeros((h, w), dtype=np.uint8)
    for v in blocks.values():
        if len(v) > 1:
            for x, y in v:
                mask[y:y+block, x:x+block] = 255

    return float(score), Image.fromarray(mask)
