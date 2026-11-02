import cv2
import pytesseract
import matplotlib.pyplot as plt
from pytesseract import Output
from pathlib import Path

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

        gray = cv2.cvtColor(sharpened, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(
            gray, 115, 255, cv2.THRESH_BINARY_INV
        )[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilate = cv2.dilate(thresh, kernel, iterations=1)

        return dilate

        

    def read_image(self, image_path):
        image = cv2.imread(str(image_path))

        if image is None:
            raise OSError(f"Unable to load image{image_path}")

        return image

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

    for image_path in location.list_images():
        image = reader.read_image(image_path)
        enhanced_image = reader.enhance_image(image)
        title = f"# Read Image: {image_path.name} #"
        
        print("#" * len(title))
        print(title)
        print("#" * len(title))

        print("\n")
        print(reader.extract_text(enhanced_image))
        cv2.imshow("Teste", enhanced_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()