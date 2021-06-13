from os import walk, chdir
from os.path import getsize
from PIL import Image

directory = input('Папка с фотографиями: ')
chdir(directory)
total_size = 0

for root, _, files in walk(directory):
    for file in files:
        path = f'{root}/{file}'
        if file.title().split('.')[-1].lower() in ['jpg', 'jpeg', 'img', 'png']:
            try:
                total_size += getsize(path)
                image = Image.open(path)
                image.save(path)
                total_size -= getsize(path)
                print(f'[+] "{file}"')
            except Exception as e:
                print(f'[-] "{file}" вызвала ошибку: {e}')

print(f'Завершено. Было сэкономлено {total_size//1048576} мегабайт.')