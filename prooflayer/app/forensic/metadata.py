import exifread
import io
import mimetypes

def extract_metadata(filename: str, content: bytes) -> dict:
    mime, _ = mimetypes.guess_type(filename)
    if mime is None:
        mime = "application/octet-stream"

    data = {"filename": filename, "mime": mime}

    if mime.startswith("image/"):
        try:
            tags = exifread.process_file(io.BytesIO(content), details=False)
            data["exif"] = {k: str(v) for k, v in tags.items()}
        except Exception:
            data["exif"] = {}

    return data
