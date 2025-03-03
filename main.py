import os
import sys
import psycopg2
from dotenv import load_dotenv
from extract_text_and_chunk_document import process_document
from embed_the_text import embed_chunks
from retrieval import retrieve_relevant_chunks
from database import create_database, create_tables, document_exists_in_db


load_dotenv()

DB_CONFIG = {
        "dbname": os.getenv("DBNAME"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT"),
    }


def main():
    print("\n🚀 Starting the RAG Pipeline...\n")

    # Step 1: Create the database if it doesn't exist
    create_database()

    # Step 2: Create the necessary tables
    create_tables()
    print("✅ Tables created successfully.")

    # Check if the document is provided
    if len(sys.argv) < 2:
        print("❌ ERROR: Please provide a document filename as an argument.")
        print("Usage: python main.py example.pdf")
        sys.exit(1)

    document_path = sys.argv[1]

    if not os.path.exists(document_path):
        print(f"❌ ERROR: The file '{document_path}' does not exist. Please check the path.")
        sys.exit(1)

    print(f"📂 Processing document: {document_path}")

    if not document_exists_in_db(document_path):
        # Step 2: Extract text and chunk
        print("\n🔍 Extracting text and chunking...")
        process_document(document_path)
        print("✅ Text extraction & chunking completed.")

        # Step 3: Embed the extracted chunks
        print("\n🧠 Generating embeddings...")
        embed_chunks()
        print("✅ Embeddings stored successfully.")

    while True:
        user_query = input("Please enter your question: ")
        if user_query.lower() == 'exit':
            break
        retrieved_results = retrieve_relevant_chunks(user_query)
        print(retrieved_results)

    print("\n✅ RAG Pipeline Completed Successfully!\n")

if __name__ == "__main__":
    main()
