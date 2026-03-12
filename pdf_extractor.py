import fitz  # PyMuPDF
import os

def extract_pdf_data(pdf_path, output_image_folder="extracted_images"):
    # 1. Create a folder to save our images if it doesn't exist
    if not os.path.exists(output_image_folder):
        os.makedirs(output_image_folder)

    # 2. Open the PDF document
    doc = fitz.open(pdf_path)
    
    extracted_text = ""
    image_counter = 1

    print(f"Processing '{pdf_path}' (Total Pages: {len(doc)})\n")

    # 3. Loop through every page in the PDF
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # --- EXTRACT TEXT ---
        # Grab the text from the current page and add it to our master string
        text = page.get_text("text")
        extracted_text += f"\n--- Page {page_num + 1} ---\n{text}"
        
        # --- EXTRACT IMAGES ---
        # Get a list of all images on this specific page
        images = page.get_images(full=True)
        
        for img_index, img in enumerate(images):
            xref = img[0] # The internal reference number for the image
            
            # Extract the raw image bytes
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"] # e.g., 'png' or 'jpeg'
            
            # Create a filename and save it to our folder
            image_filename = f"{output_image_folder}/image_{image_counter}_page_{page_num + 1}.{image_ext}"
            
            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)
                
            print(f"Saved: {image_filename}")
            image_counter += 1

    print("\nExtraction Complete!")
    return extracted_text

# --- Run the function ---
if __name__ == "__main__":
    pdf_file = "sample.pdf" # Make sure this matches your PDF's name
    
    all_text = extract_pdf_data(pdf_file)
    
    # Print a tiny preview of the text we extracted
    print("\nPreview of extracted text:")
    print(all_text[:300] + "...\n")