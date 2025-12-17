from io import BytesIO
from PIL import Image
import base64

from app.forensic.metadata import extract_metadata
from app.forensic.hashing import sha256_bytes
from app.forensic.ela import run_ela
from app.forensic.clone_detect import detect_clone_regions
from app.forensic.compression import compression_anomaly_score


def analyze_file(filename: str, content: bytes) -> dict:
    metadata = extract_metadata(filename, content)
    file_hash = sha256_bytes(content)

    is_image = True
    try:
        img = Image.open(BytesIO(content)).convert("RGB")
    except Exception:
        is_image = False
        img = None

    checks = []
    heatmap = None

    if is_image:
        ela_img, ela_score = run_ela(img)
        clone_score, clone_mask = detect_clone_regions(img)
        comp_score = compression_anomaly_score(img)

        checks = [
            {"check": "ELA", "score": ela_score},
            {"check": "CLONE", "score": clone_score},
            {"check": "COMPRESSION", "score": comp_score},
        ]

        buf = BytesIO()
        ela_img.save(buf, format="PNG")
        heatmap = base64.b64encode(buf.getvalue()).decode()

        agg = (ela_score + clone_score + comp_score) / 3
        integrity = round(100 - agg * 100, 2)
    else:
        integrity = 100.0

    return {
        "filename": filename,
        "hash": file_hash,
        "metadata": metadata,
        "integrity_score": integrity,
        "checks": checks,
        "tamper_heatmap": heatmap,
    }
