import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("CHEFFY_DATA_DIR", BASE_DIR)
DB_PATH = os.environ.get("CHEFFY_DB_PATH", os.path.join(DATA_DIR, "contratos.db"))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
UPLOAD_IMAGE_DIR = os.path.join(IMAGE_DIR, "uploads")
DEFAULT_IMAGE = os.path.join(BASE_DIR, "BuffentInfantilCompleto.jpeg")
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_UPLOAD_SIZE = 16 * 1024 * 1024
API_TOKEN = os.environ.get("CHEFFY_API_TOKEN", "")
