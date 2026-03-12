import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def ask_pdf(question):
    # 2. Load the Google Models and Database
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    
    # 3. Create the Database Searcher
    retriever = vector_db.as_retriever(search_kwargs={"k": 2}) 
    llm = llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    print(f"Thinking about: '{question}'...\n")

    # --- THE MANUAL RAG PIPELINE ---
    
    # Step A: Search the database for the 2 best text chunks
    found_docs = retriever.invoke(question)
    
    # Step B: Glue those chunks together into one big string
    context_text = "\n\n".join([doc.page_content for doc in found_docs])
    
    # Step C: Build the prompt and send it to Gemini
    master_prompt = f"""
    You are a highly intelligent and thorough document assistant. 
    Read the following extracted context from a document carefully.
    
    Context:
    {context_text}
    
    Question: {question}
    
    Instructions:
    1. Answer the question using ONLY the provided context.
    2. If the answer is a list (like skills or concepts), extract EVERY SINGLE ITEM mentioned in the context. Do not stop early.
    3. Format your answer clearly using bullet points.
    4. If the answer is truly not in the context, say "I cannot find the answer in the document."
    """
    
    response = llm.invoke(master_prompt)
    
    # --- PRINT THE RESULTS ---
    print("--- GENERATED ANSWER ---")
    print(response.content) # Gemini's final answer
    print("------------------------\n")

    print("--- ATTACHED IMAGES ---")
    found_image = False
    
    # Step D: Loop through the database chunks we found and check their backpacks!
    for doc in found_docs:
        if "image_url" in doc.metadata:
            print(f"Found relevant image: {doc.metadata['image_url']}")
            found_image = True
            
    if not found_image:
        print("No images were relevant to this specific question.")
    print("------------------------\n")
    # --- PREVIOUS CODE REMAINS THE SAME ---
    response = llm.invoke(master_prompt)
    
    # --- NEW: RETURN THE DATA INSTEAD OF PRINTING ---
    found_image_path = None
    
    for doc in found_docs:
        if "image_url" in doc.metadata:
            found_image_path = doc.metadata['image_url']
            break # Just grab the first relevant image we find
            
    # Return a neat dictionary!
    return {
        "answer": response.content,
        "image": found_image_path
    }