import os
import PyPDF2
import pandas as pd
import docx
from langchain.text_splitter import RecursiveCharacterTextSplitter
import psycopg2
from dotenv import load_dotenv


load_dotenv()

DB_CONFIG = {
        "dbname": os.getenv("DBNAME"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT"),
    }

def extract_text(file_path):
    """Extracts text from different document formats."""
    _, ext = os.path.splitext(file_path)
    
    if ext == ".pdf":
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    
    elif ext in [".csv", ".xlsx"]:
        df = pd.read_csv(file_path) if ext == ".csv" else pd.read_excel(file_path)
        text = " ".join(df.astype(str).values.flatten())
    
    elif ext == ".docx":
        doc = docx.Document(file_path)
        text = " ".join([para.text for para in doc.paragraphs])
    
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    
    else:
        raise ValueError("Unsupported file format.")
    
    return text

def chunk_text(text):
    """Splits text into manageable chunks."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_text(text)

def store_chunks(file_name, chunks):
    """Stores extracted chunks into the database."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("INSERT INTO document_metadata (title, source) VALUES (%s, %s) RETURNING document_id", (file_name, "Uploaded Document"))
    document_id = cur.fetchone()[0]

    for i, chunk in enumerate(chunks):
        cur.execute("INSERT INTO chunk (document_id, chunk_number, chunk_text) VALUES (%s, %s, %s)", (document_id, i, chunk))

    conn.commit()
    cur.close()
    conn.close()

def process_document(file_path):
    text = extract_text(file_path)
    chunks = chunk_text(text)
    store_chunks(os.path.basename(file_path), chunks)
    print(f"Processed {file_path}: {len(chunks)} chunks stored.")

# Example usage
# process_document("example.pdf")
