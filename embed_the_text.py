import cohere
from langchain_postgres import PGVector
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

DB_CONFIG = {
        "dbname": os.getenv("DBNAME"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT"),
    }

# Initialize Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY"))

def get_embedding(text):
    """Generates embeddings using Cohere with search_document input type."""
    response = co.embed(
        texts=[text], 
        model="embed-english-v3.0",
        input_type="search_document",  # Specify input type for vector database
        embedding_types=["float"]  # Specify float embeddings
    )
    # Correctly extract the float embedding
    return response.embeddings.float[0]

def embed_chunks():
    """Fetches unembedded chunks, embeds them, and stores embeddings in the database."""
    # Connect to the database
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Fetch all unembedded chunks
    cur.execute("SELECT chunk_id, chunk_text FROM chunk WHERE chunk_id NOT IN (SELECT chunk_id FROM embedding)")
    chunks = cur.fetchall()

    # Initialize PGVector for embedding storage
    connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    vector_store = PGVector(
        connection=connection_string,  # Pass the connection string
        embeddings=co,  # Pass the Cohere client
        collection_name="collection",  # Specify the collection name
    )

    # Prepare texts, embeddings, and metadata
    texts = [chunk_text for _, chunk_text in chunks]
    embeddings = [get_embedding(chunk_text) for _, chunk_text in chunks]
    metadatas = [{"chunk_id": chunk_id} for chunk_id, _ in chunks]

    # Store the embeddings
    vector_store.add_embeddings(
        texts=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    conn.commit()
    cur.close()
    conn.close()
    print(f"Embedded {len(chunks)} chunks.")