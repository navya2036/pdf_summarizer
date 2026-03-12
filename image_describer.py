import os
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_image_descriptions(image_folder):
    print(f"Starting Local OCR Analysis on images in '{image_folder}'...")
    descriptions = {}
    
    for filename in os.listdir(image_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(image_folder, filename)
            print(f"Scanning {filename} for text...")

            try:
                # --- ZERO API LIMITS. RUNS LOCALLY. ---
                extracted_text = pytesseract.image_to_string(Image.open(image_path))
                
                if extracted_text.strip():
                    descriptions[filename] = f"[IMAGE TEXT CONTENT]: {extracted_text.strip()}"
                    print(f"Extracted text from {filename}")
                else:
                    descriptions[filename] = "[IMAGE]: This image contains no readable text."
                    print(f"No text found in {filename}, skipping.")
                    
            except Exception as e:
                print(f"OCR failed for {filename}. Error: {e}")

    return descriptions

if __name__ == "__main__":
    get_image_descriptions("extracted_images")