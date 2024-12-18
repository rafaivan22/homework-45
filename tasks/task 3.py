from PIL import Image
import os

class JPEGCompressor:
    def __init__(self):
        self.image = None
        self.quality = 100  # По умолчанию качество максимальное, без сжатия

    def load(self, filepath):
        # Проверить существование файла
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} not found")

        try:
            # Проверяем формат и загружаем изображение
            image = Image.open(filepath)
            if image.format != 'JPEG':
                raise TypeError("Only JPEG format is supported")
            self.image = image
        except Exception:
            raise TypeError("The file could not be loaded as an image")

    def compress(self, quality):
        # Проверяем, загружено ли изображение
        if self.image is None:
            raise FileNotFoundError("No image loaded")

        # Проверяем корректность уровня качества
        if not (0 <= quality <= 95):
            raise ValueError("Quality must be between 0 and 95")

        self.quality = quality

    def save(self, filepath):
        # Проверяем, загружено ли изображение
        if self.image is None:
            raise FileNotFoundError("No image loaded")

        # Сохранение изображения с заданным уровнем качества
        self.image.save(filepath, format='JPEG', quality=self.quality, optimize=True)
