from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import shutil
from ask_question import ask_pdf
from build_database import build_real_database 

# --- NEW IMPORTS: For safe database clearing ---
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

app = Flask(__name__)
CORS(app) 

# Create a safe folder to hold uploaded files
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- NEW ROUTE: Handle File Uploads ---
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    if file and file.filename.endswith('.pdf'):
        print(f"Receiving new file: {file.filename}")
        
        # 1. Save the new PDF
        filepath = os.path.join(UPLOAD_FOLDER, "current_doc.pdf")
        file.save(filepath)
        
        # 2. Empty the old database
        if os.path.exists("./chroma_db"):
            try:
                print("Emptying the old database...")
                embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                old_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
                old_db.delete_collection()
            except Exception as e:
                print(f"Warning: Could not clear old database natively: {e}")
                
        # --- NEW: CLEAR THE OLD IMAGES! ---
        image_folder = "./extracted_images"
        if os.path.exists(image_folder):
            print("Sweeping up old extracted images...")
            shutil.rmtree(image_folder)      # Deletes the folder and everything inside
        os.makedirs(image_folder, exist_ok=True) # Creates a brand new, empty folder
        # ----------------------------------
                
        # 3. Build the new database
        try:
            print("Building new vector database... this might take a minute...")
            build_real_database(filepath)
            return jsonify({"message": "File processed successfully! The AI is ready for your questions."})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    return jsonify({"error": "Please upload a valid PDF file"}), 400

# --- PREVIOUS ROUTES REMAIN THE SAME ---
@app.route('/api/ask', methods=['POST'])
def handle_question():
    data = request.json
    user_question = data.get("question")
    if not user_question:
        return jsonify({"error": "No question provided"}), 400
    result = ask_pdf(user_question)
    return jsonify(result)

@app.route('/api/images/<filename>')
def serve_image(filename):
    image_path = os.path.join("extracted_images", filename)
    if os.path.exists(image_path):
        return send_file(image_path)
    return jsonify({"error": "Image not found"}), 404

if __name__ == '__main__':
    print("Starting Python API Server on port 5000...")
    app.run(port=5000, debug=True)