# Advanced RAG - Document Retrieval and Embedding Tool

## 🚀 Overview
Advanced RAG is a sophisticated document processing and retrieval tool that leverages **Cohere embeddings** and **PostgreSQL vector search** to provide powerful semantic document analysis. The system extracts, embeds, and retrieves document chunks with high precision and efficiency.

---

## 🌟 Features

### 🔍 **Advanced Document Processing**
- Extracts text from multiple file formats: **PDF, DOCX, CSV, TXT**
- Chunks documents into **manageable sizes** for optimal retrieval
- Generates **high-quality embeddings** using Cohere's state-of-the-art models

### 🗄️ **Dynamic Database Integration**
- Configurable **PostgreSQL connection**
- Secure credential management with `.env` files
- Utilizes `pgvector` for efficient vector similarity search

### 🧠 **Powerful Semantic Search**
- Generates embeddings with **Cohere's embed-english-v3.0 model**
- Performs advanced **similarity searches** across document chunks
- Retrieves the **most relevant information** quickly and accurately

### 📦 **Flexible & Modular Architecture**
- **Easily extensible** for custom enhancements
- Supports various document types
- Designed for **scalability and performance**

---

## 🛠️ Requirements

### 🔹 **Software Requirements**
- Python **3.8+**
- PostgreSQL **12+**
- `pgvector` extension for vector-based search
- Cohere API Key

### 🔹 **Key Python Packages**
- `cohere`: AI-powered embeddings
- `langchain-postgres`: Vector database integration
- `psycopg2-binary`: PostgreSQL database connection
- `python-dotenv`: Environment variable management
- Document processing libraries: `pdfplumber`, `python-docx`, `PyPDF2`

---

## ⚙️ Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/nathe444/PG-Vector_RAG.git
cd PG-Vector_RAG
```

### 2. Create Virtual Environment
```bash
python -m venv myenv
source myenv/bin/activate  # Unix/macOS
myenv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration

#### Environment Variables

Create a .env file in the project root with the following configuration:
```bash
DBNAME=
USER=
PASSWORD=
HOST=
PORT=
```
### 5. Usage

#### Processing Documents
```bash
python main.py example.pdf

```


#### Integrating pgvector with PostgreSQL
To use pgvector for vector similarity search in PostgreSQL, follow these steps:

1. Connect to your PostgreSQL database.

2. Run the following command to create the pgvector extension:
```sql
CREATE EXTENSION IF NOT EXISTS pgvector;
```

for further checking go to https://github.com/pgvector/pgvector

---
