import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('config.env')


class FileSystemIterator:
    def __init__(self, path, mode='files', pattern=""):
        self.path = Path(path)
        self.mode = mode
        self.pattern = pattern

        if not self.path.is_dir():
            raise NotADirectoryError(f"Задан неверный путь: {path}")

        if self.mode not in ['files', 'dirs', 'both']:
            raise ValueError("mode должен быть 'files', 'dirs', или 'both'")

    def __iter__(self):
        self._walk_gen = self.generator_func(self.path, self.mode, self.pattern)
        return self

    def __next__(self):
        return next(self._walk_gen)

    def generator_func(self, path, mode, pattern):
        with os.scandir(path) as scan:
            for entry in scan:
                # Проверка на то, является ли путь - директорией
                if entry.is_dir():
                    dir_path = Path(entry.path)
                    # Вывод пути до директории
                    if (mode in ['dirs', 'both']) and (pattern in dir_path.name):
                        yield dir_path
                    # Рекурсивный обход поддиректорий
                    if mode in ['dirs', 'both', 'files']:
                        yield from self.generator_func(dir_path, mode, pattern)
                # Проверка на то, является ли путь - файлом
                elif entry.is_file() and mode in ['files', 'both'] and (pattern in entry.name):
                    yield Path(entry.path)

# Загрузка пути для итерации
filepath = os.getenv('FILEPATH')

try:
    iterator = FileSystemIterator(filepath, mode='files', pattern='')
    for file_path in iterator:
        print(file_path)
except (FileNotFoundError, NotADirectoryError, ValueError) as e:
    print(f"Ошибка: {e}")



