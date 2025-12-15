import uuid
import os

UPLOAD_DIR = "uploads"
MODEL_DIR = "backend/models"

def generate_id() -> str:
    return str(uuid.uuid4())

def get_file_path(file_id: str) -> str:
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    for fname in os.listdir(UPLOAD_DIR):
        if fname.startswith(file_id):
            return os.path.join(UPLOAD_DIR, fname)
    return None

def save_upload_file(file_content: bytes, filename: str) -> str:
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_id = generate_id()
    ext = os.path.splitext(filename)[1]
    save_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
    
    with open(save_path, "wb") as f:
        f.write(file_content)
        
    return file_id
