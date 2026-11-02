from PIL import Image

import pytesseract
import enum
import keras_ocr
from matplotlib import pyplot as plt

class OS(enum.Enum):
    Linux = 0
    Windows = 1

class Language(enum.Enum):
    ENG = 'eng'
    POR = 'por'


class ImageReader:

    def __init__(self, os: OS):
        if os == OS.Linux:
            print('Running on: LINUX\n')

        if os == OS.Windows:
            windows_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            pytesseract.tesseract_cmd= windows_path
            print('Running on: WINDOWS\n')

    def extract_text(self, image: str, lang: str, config: str = "") -> str:
        img = Image.open(image)
        extracted_text = pytesseract.image_to_string(img, lang=lang, config=config)
        return extracted_text

    def tesseract_config(self) -> str:
        config = ("")
        config2 = (
                "--psm 8 "
                "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
                "-c load_system_dawg=0 "
                "-c load_freq_dawg=0"
            )
        return config
    
if __name__ == '__main__':
    ir = ImageReader(OS.Linux)
    text = ir.extract_text('images/teste.png', lang='por', config=ir.tesseract_config())
    print(text)

    print("\n-----------------------\n")
    print("Teste 2\n")

    pipeline = keras_ocr.pipeline.Pipeline()

    images = [keras_ocr.tools.read(img) for img in ['images/Imagem.jpeg']]

    print(images)
    