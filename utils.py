from pathlib import Path


IMAGE_FILES_FORMATS = 'jpg', 'jpeg', 'img', 'png', 'bmp', 'ico'


def is_image(file_path: str) -> bool:
    return file_path.lower().endswith(IMAGE_FILES_FORMATS)


def to_megabytes(bytes_: int) -> float:
    return bytes_ / (1024 * 1024)


def get_file_size(file_path: str) -> int:
    return Path(file_path).stat().st_size
