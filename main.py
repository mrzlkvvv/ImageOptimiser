#!/usr/bin/python3

from argparse import ArgumentParser, Namespace
from concurrent.futures import ThreadPoolExecutor
from os import cpu_count
from pathlib import Path
from secrets import token_hex
from shutil import rmtree
from time import time
from typing import Iterator

from PIL import Image, ImageOps

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.ico', '.webp', '.tif', '.tiff'}
SIZE_UNITS = ('B', 'KB', 'MB', 'GB', 'TB')

MAX_WORKERS = min(16, (cpu_count() or 1) * 2)

TEMP_DIR = Path('.temp')


def process_image(image_path: Path) -> int:
    """
    Process an image by removing EXIF data and saving it.
    Returns size_delta (in bytes)
    """

    size_before = image_path.stat().st_size

    try:
        with Image.open(image_path) as image:
            # Get file extension: PIL format with path suffix fallback
            file_extension = (
                image.format.lower()
                if image.format is not None
                else image_path.suffix[1:].lower()
            )

            # Transpose image if it is rotated through EXIF
            if file_extension in {'jpg', 'jpeg', 'tif', 'tiff'}:
                image = ImageOps.exif_transpose(image)

            # Save temp image without EXIF
            temp_path = TEMP_DIR / f'{token_hex(12)}.{file_extension}'
            image.save(temp_path, optimize=True, quality=95)

            # Calculate size reduction
            size_after = temp_path.stat().st_size
            size_delta = size_before - size_after

            # Replace the original image with the new one if the file size has decreased
            if size_delta > 0:
                temp_path.replace(image_path)
                print(f'[+] "{image_path}"')
            else:
                temp_path.unlink()
                print(f'[=] "{image_path}"')

            return size_delta

    except OSError as error:
        print(f'[-] "{image_path}": {error}')
        return 0


def get_image_paths(root_path: Path) -> Iterator[Path]:
    """Recursively yield image file paths in the directory"""

    for path in root_path.rglob('*'):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            yield path


def get_formatted_size(bytes_: int) -> str:
    """Convert bytes to human-readable format (e.g., '2.3 MB')"""

    size = float(bytes_)
    unit_index = 0

    while size >= 1024 and unit_index < len(SIZE_UNITS) - 1:
        size /= 1024.0
        unit_index += 1

    return f'{size:.1f} {SIZE_UNITS[unit_index]}'


def parse_args() -> Namespace:
    parser = ArgumentParser(
        description='This script removes metadata from images',
    )

    parser.add_argument(
        '-d',
        '--directory',
        type=Path,
        help='directory with images',
        required=True,
    )

    parser.add_argument(
        '-w',
        '--workers',
        type=int,
        default=MAX_WORKERS,
        help='number of worker threads for parallel processing',
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    dir_path = Path(args.directory)
    if not dir_path.is_dir():
        print(f'"{dir_path}" is not a valid directory')
        return

    start_time = time()

    TEMP_DIR.mkdir(exist_ok=True)

    try:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            total_size_delta = sum(
                executor.map(process_image, get_image_paths(dir_path))
            )
    finally:
        rmtree(TEMP_DIR, ignore_errors=True)

    elapsed = time() - start_time

    if total_size_delta > 0:
        formatted_size = get_formatted_size(total_size_delta)
        print(f'Saved {formatted_size} of disk space in {elapsed:.2f} seconds')
    else:
        print(f'No disk space was saved in {elapsed:.2f} seconds :(')


if __name__ == '__main__':
    main()
