from pathlib import Path
from datetime import datetime
from PIL import Image

# Work with these extensions: {'jpg', 'jpeg', 'img', 'png', 'bmp', 'ico'}
# and it's uppercase analogs
IMAGE_FILES_PATTERN = '**/*.[jJiIbBpP][mMnNcCpP][oOeEgGpP]'


def get_dir_size(dir_path):
    size = 0
    for file_path in Path(dir_path).glob(IMAGE_FILES_PATTERN):
        size += Path(file_path).stat().st_size
    return size


def process_image(image_path):
    try:
        image = Image.open(image_path)
        image.save(image_path)
        print(f'[+] "{image_path}"')
    except Exception as exception:
        print(f'[-] "{image_path}": {exception}')


def main():
    dir_path = input('Path to directory with photos: ')
    start_time = datetime.now()
    size_before = get_dir_size(dir_path)

    for file_path in Path(dir_path).glob(IMAGE_FILES_PATTERN):
        process_image(file_path)

    size_after = get_dir_size(dir_path)
    print('Was saved '
          f'{(size_before-size_after)//1048576} MiB of disk space '
          f'in {(datetime.now()-start_time).seconds} seconds.')


if __name__ == '__main__':
    main()
