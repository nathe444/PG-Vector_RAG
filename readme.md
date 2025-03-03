

- Python **3.7+**
- PostgreSQL **12+**
- `pgvector` extension for vector-based search


### 🔹 **Python Packages**
Ensure you have the following dependencies installed:
- `langchain-postgres`
- `langchain-community`
- `python-dotenv`
- `PyPDF2`
- `pandas`
- `python-docx`
- `psycopg2`
- `huggingface_hub`


---


## ⚙️ Installation Guide


### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/nathe444/PG-Vector_RAG.git
cd PG-Vector_RAG
```


### 2. Create a Virtual Environment
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
python main.py path_to_your_document
```
eg. python main.py test.pdf

put the document you want to embed in the root folder



#### Integrating pgvector with PostgreSQL
To use pgvector for vector similarity search in PostgreSQL, follow these steps:


1. Connect to your PostgreSQL database.


2. Run the following command to create the pgvector extension:
```sql
CREATE EXTENSION IF NOT EXISTS pgvector;
```


for further checking go to https://github.com/pgvector/pgvector

### 🗄️ **Dynamic Database Integration**
- Configurable **PostgreSQL connection**
- Environment-based configuration for flexibility
- Secure credential management with `.env` files


### 🧠 **Powerful Semantic Search**
- Generates embeddings with **Hugging Face models**
- Performs **similarity searches** across document chunks
- Retrieves the **most relevant information** quickly


### 📦 **Flexible & Modular Architecture**
- **Easily extensible** for custom enhancements
- Supports various document types
- Designed for **scalability and performance**
