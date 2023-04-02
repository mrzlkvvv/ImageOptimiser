#!/usr/bin/python3

"""This script removes EXIF-data from images in the specified directory."""

import os
from time import time
from pathlib import Path

from PIL import Image, ImageOps


IMAGE_FILES_FORMATS = 'jpg', 'jpeg', 'img', 'png', 'bmp', 'ico'


def is_image(file_path: str) -> bool:
    return file_path.lower().endswith(IMAGE_FILES_FORMATS)


def to_megabytes(bytes_: int) -> float:
    return bytes_ / (1024 * 1024)


def get_file_size(file_path: str) -> int:
    return Path(file_path).stat().st_size


def remove_exif(image_path: str) -> int:
    """Removes EXIF-data from the image. Returns size delta in bytes"""

    size_before = get_file_size(image_path)

    try:
        image = Image.open(image_path)

        # Transpose image if it is rotated through EXIF
        image = ImageOps.exif_transpose(image)

        # Delete original image
        os.remove(image_path)

        # Save image without EXIF-info
        image.save(image_path)

        print(f'[+] "{image_path}"')
    except OSError as error:
        print(f'[-] "{image_path}": {error}')

    size_after = get_file_size(image_path)

    return size_before - size_after


def main() -> None:
    """Recursive scanning of the directory with images and reducing their size"""

    dir_path = input('Path to directory with photos: ')

    start_time = time()
    size_delta = 0

    for current_dir, _, files in os.walk(dir_path):
        for file in files:
            if is_image(file):
                size_delta += remove_exif(f'{current_dir}/{file}')

    time_delta = int(time() - start_time)

    print('Was saved '
          f'{to_megabytes(size_delta):.1f} MB of disk space '
          f'in {time_delta} seconds.')


if __name__ == '__main__':
    main()
