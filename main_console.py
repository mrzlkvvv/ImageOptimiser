from os import walk, chdir
from os.path import getsize
from PIL import Image


def delete_meta(image_path):
    try:
        image = Image.open(image_path)
        image.save(image_path)
        print(f'[+] "{image_path}"')
    except Exception as e:
        print(f'[-] "{image_path}" вызвала ошибку: {e}')


if __name__ == '__main__':
    total_size = 0

    for root, _, files in walk(input('Папка с фотографиями: ')):
        for file in files:
            if file.split('.')[-1].lower() in {'jpg', 'jpeg', 'img', 'png', 'bmp', 'ico'}:
                full_path = f'{root}/{file}'
                total_size += getsize(full_path)
                delete_meta(full_path)
                total_size -= getsize(full_path)

    print(f'Завершено. Было сэкономлено {total_size//1048576} МБ.')
