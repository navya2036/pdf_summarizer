import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# Look at this! We are importing the powerful functions you already wrote.
from pdf_extractor import extract_pdf_data
from image_describer import get_image_descriptions

def build_real_database(pdf_filename):
    print("--- STEP 1: EXTRACTING RAW DATA ---")
    # Go get the real text from the PDF
    real_pdf_text = extract_pdf_data(pdf_filename)
    
    print("\n--- STEP 2: ANALYZING IMAGES WITH AI ---")
    # Go get the smart descriptions of any images it found
    real_image_summaries = get_image_descriptions("extracted_images")
    
    print("\n--- STEP 3: PACKAGING FOR THE DATABASE ---")
    documents = []
    
    # Package the main PDF text
    if real_pdf_text.strip():
        documents.append(Document(page_content=real_pdf_text, metadata={"source": "PDF_Text"}))
    
    # Package the smart image summaries
    for img_name, summary in real_image_summaries.items():
        # Let's save the full path so it's perfectly ready for your frontend later!
        full_image_path = f"extracted_images/{img_name}"
        documents.append(Document(page_content=summary, metadata={"source": "Image", "image_url": full_image_path}))

    print(f"Packaged {len(documents)} total core documents.")

    # Chunk the text (Notice I increased the chunk size slightly for real, larger paragraphs)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunked_documents = text_splitter.split_documents(documents)
    print(f"Split into {len(chunked_documents)} searchable chunks.")

    print("\n--- STEP 4: BUILDING THE VECTOR DATABASE ---")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    db_directory = "./chroma_db"
    vector_db = Chroma.from_documents(
        documents=chunked_documents,
        embedding=embeddings,
        persist_directory=db_directory
    )

    print(f"\nSUCCESS! Real database built and saved to '{db_directory}'.")
    return vector_db

# if __name__ == "__main__":
#     # Make sure you have a real PDF named 'sample.pdf' in your folder!
#     build_real_database("sample.pdf")