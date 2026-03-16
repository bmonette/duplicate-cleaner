import hashlib
from pathlib import Path


def calculate_hash(file_path, chunk_size=8192):
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File does not exist: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(chunk_size):
            sha256.update(chunk)

    return sha256.hexdigest()
