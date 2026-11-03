import cv2
import pytesseract
import matplotlib.pyplot as plt
from pytesseract import Output
from pathlib import Path
import easyocr

class ImageLocation:
    
    def __init__(self, image_dir=None):
        if image_dir is None:
            image_dir = Path(__file__).resolve().parent / "images"

        self.image_dir = Path(image_dir)
    
    def list_images(self):
        return [path for path in self.image_dir.iterdir() if path.is_file()]

        

class ImageReader:

    def enhance_image(self, img):
        blurred = cv2.GaussianBlur(img, (0, 0), 3)
        sharpened = cv2.addWeighted(img, 1.5, blurred, -0.5, 0)

        thresh = cv2.threshold(sharpened, 115, 255, cv2.THRESH_BINARY_INV)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        dilate = cv2.dilate(thresh, kernel, iterations=2)
        final = cv2.threshold(dilate, 115, 255, cv2.THRESH_BINARY_INV)[1]

        return final

        

    def read_image(self, image_path):
        image = cv2.imread(str(image_path))

        if image is None:
            raise OSError(f"Unable to load image{image_path}")

        return image

    def read_image_easyocr(self, image_path):

        image_ocr = reader.readtext(str(image_path), allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        if image_ocr is None:
            raise OSError(f"Unable to load image{image_path}")

        return image_ocr

    def custom_config(self) -> str:
        config = (
            "--psm 7 --oem 3 "
            "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
            "-c load_system_dawg=0 -c load_freq_dawg=0"
        )
        
        return config

    def extract_text(self, image_rgb):
        extracted_text = pytesseract.image_to_string(image_rgb, lang="por", config=self.custom_config())
        return extracted_text

if __name__ == '__main__':
    location = ImageLocation()
    reader = ImageReader()
    easy_reader = easyocr.Reader(["en"])

    for image_path in location.list_images():
        image = reader.read_image(image_path)
        enhanced_image = reader.enhance_image(image)
        image_ocr = easy_reader.readtext(enhanced_image)
        image_ocr_enhanced = easy_reader.readtext(enhanced_image)
        title = f"# Read Image: {image_path.name} #"
        
        print("#" * len(title))
        print(title)
        print("#" * len(title))

        print("\n")
        print("Tesserect: ")
        print(reader.extract_text(enhanced_image))
        print("\n")

        print("EasyOCR: ")

        if not image_ocr:
            print("EasyOCR não encontrou texto nesta imagem.")
            continue

        for box, text, confidence in image_ocr:
            print(f"Texto: {text} | Confiança: {confidence:.2f}")
        
        print("\n")

        print("EasyOCR Enhanced: ")
        
        if not image_ocr_enhanced:
            print("EasyOCR não encontrou texto nesta imagem.")
            continue

        for box, text, confidence in image_ocr_enhanced:
            print(f"Texto: {text} | Confiança: {confidence:.2f}")
        
        print("\n")