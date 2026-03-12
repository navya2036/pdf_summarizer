# ✨ PDF AI Assistant

An intelligent full-stack web application that lets you chat with your PDF documents.

This project uses a hybrid AI architecture. To improve privacy, speed, and resilience against cloud API rate limits, it processes documents, extracts image text with OCR, and builds the vector database locally. It only calls the cloud, using Google Gemini 2.5 Flash, for the final reasoning step when answering questions.

Coupled with a modern React frontend, the app provides a polished chat workflow for uploading PDFs, indexing their content, and asking document-grounded questions.

---

## 🚀 Features

- Sleek React chat interface for uploading PDFs and asking questions.
- Smart hybrid pipeline using local embeddings and OCR with cloud reasoning.
- Local image parsing with Tesseract OCR to read text from diagrams and screenshots inside PDFs.
- Free local vector database powered by ChromaDB and HuggingFace `all-MiniLM-L6-v2` embeddings.
- Context-aware answers generated with LangChain and Google Gemini 2.5 Flash.
- Automatic cleanup of old vector data and extracted images when a new PDF is uploaded.

---

## 🛠️ Tech Stack

**Frontend**

- React
- Vite
- Inline custom styling for the chat UI

**Backend**

- Python
- Flask
- LangChain
- ChromaDB
- HuggingFace sentence-transformers
- Tesseract OCR via `pytesseract`
- Google Gemini via `langchain-google-genai`
- PyMuPDF for PDF text and image extraction

---

## ⚙️ Installation & Setup

### 1. Prerequisites

Make sure these are installed first:

- Node.js
- Python 3.8+
- Tesseract OCR

Tesseract installation:

- Windows: Install the 64-bit build from https://github.com/UB-Mannheim/tesseract/wiki and keep the default path at `C:\Program Files\Tesseract-OCR\tesseract.exe`.
- macOS: Run `brew install tesseract`.

Note: the current OCR configuration in the backend is hardcoded to the default Windows Tesseract path.

### 2. Clone the Repository

```bash
git clone https://github.com/navya2036/pdf_summarizer.git
cd pdf_summarizer
```

### 3. Backend Setup

Create and activate a virtual environment if you want an isolated Python setup:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the backend dependencies:

```bash
pip install flask flask-cors python-dotenv pymupdf langchain langchain-community langchain-google-genai langchain-huggingface langchain-text-splitters sentence-transformers chromadb pytesseract pillow
```

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_api_key_here
```

### 4. Frontend Setup

Open a second terminal and install the frontend dependencies:

```bash
cd frontend
npm install
```

---

## 🏃 Running the Application

Run the backend and frontend in separate terminals.

### Terminal 1: Backend

From the project root:

```bash
python server.py
```

The Flask API starts on `http://127.0.0.1:5000`.

### Terminal 2: Frontend

From the `frontend` folder:

```bash
npm run dev
```

Vite will print a local development URL, usually `http://localhost:5173`.

---

## 🧠 How It Works

1. **Upload**: The React frontend sends the selected PDF to the Flask backend.
2. **Extraction**: `pdf_extractor.py` extracts page text and saves embedded images into `extracted_images/`.
3. **Local OCR**: `image_describer.py` uses Tesseract to read text from extracted images.
4. **Local Embedding**: `build_database.py` chunks the text and OCR results, then stores embeddings in a local ChromaDB database.
5. **Retrieval and Answering**: `ask_question.py` retrieves the most relevant chunks and sends the prompt to Gemini for the final answer.

---

## 📁 Project Structure

```text
.
├── ask_question.py
├── build_database.py
├── image_describer.py
├── pdf_extractor.py
├── server.py
├── chroma_db/
├── extracted_images/
├── uploads/
└── frontend/
    ├── package.json
    └── src/
```

---

## 🔐 Notes

- Each new PDF upload clears the previous vector database and extracted images.
- Answers are grounded in retrieved document context rather than general chat history.
- Image OCR is performed locally before retrieval.
