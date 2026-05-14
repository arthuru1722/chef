import io
import os

from flask import abort
from werkzeug.utils import secure_filename

from config import ALLOWED_IMAGE_EXTENSIONS, BASE_DIR, DEFAULT_IMAGE, IMAGE_DIR
from database import get_image, insert_image, list_uploaded_images


def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def is_db_image_ref(image_ref):
    return bool(image_ref and image_ref.startswith("db:"))


def normalize_image_ref(image_ref):
    if not image_ref:
        return ""
    if image_ref.startswith(("db:", "path:")):
        return image_ref
    return f"path:{image_ref}"


def list_image_options():
    os.makedirs(IMAGE_DIR, exist_ok=True)
    images = []
    for root, _, files in os.walk(IMAGE_DIR):
        for filename in files:
            if allowed_image(filename):
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, BASE_DIR).replace(os.sep, "/")
                images.append({
                    "value": f"path:{rel_path}",
                    "label": rel_path,
                    "url": f"/{rel_path}",
                })

    for image in list_uploaded_images():
        images.append({
            "value": f"db:{image['id']}",
            "label": f"upload/{image['nome']}",
            "url": f"/uploaded-images/{image['id']}",
        })

    return sorted(images, key=lambda item: item["label"].lower())


def selected_image_ref(form, files, current_ref=""):
    mode = form.get("image_mode", "none")
    current_ref = normalize_image_ref(current_ref)
    if mode == "existing":
        image_ref = form.get("existing_image", "")
        if resolve_image_source(image_ref):
            return image_ref
        return current_ref or ""

    if mode == "upload":
        file = files.get("new_image")
        if file and file.filename and allowed_image(file.filename):
            filename = secure_filename(file.filename)
            image_id = insert_image(
                filename,
                file.mimetype or "application/octet-stream",
                file.read(),
            )
            return f"db:{image_id}"
        return current_ref or ""

    return ""


def resolve_image_source(image_ref):
    image_ref = normalize_image_ref(image_ref)
    if not image_ref:
        return None

    if image_ref.startswith("path:"):
        rel_path = image_ref.removeprefix("path:")
        full_path = os.path.abspath(os.path.join(BASE_DIR, rel_path))
        if os.path.commonpath([BASE_DIR, full_path]) == BASE_DIR and os.path.exists(full_path):
            return full_path
        return None

    if is_db_image_ref(image_ref):
        image = get_image(int(image_ref.removeprefix("db:")))
        if image:
            stream = io.BytesIO(image["conteudo"])
            stream.name = image["nome"]
            return stream
        return None

    full_path = os.path.abspath(os.path.join(BASE_DIR, image_ref))
    if os.path.commonpath([BASE_DIR, full_path]) == BASE_DIR and os.path.exists(full_path):
        return full_path

    return None


def default_image_source():
    return DEFAULT_IMAGE if os.path.exists(DEFAULT_IMAGE) else None


def send_uploaded_image(image_id):
    image = get_image(image_id)
    if not image:
        abort(404)
    return image
