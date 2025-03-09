import cohere
from langchain_postgres import PGVector
from dotenv import load_dotenv
from format_user_question import format_user_question
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
    """Generates an embedding for the query using Cohere."""
    response = co.embed(
        texts=[text], 
        model="embed-english-v3.0",
        input_type="search_query",  # Specify input type for search queries
        embedding_types=["float"]  # Specify float embeddings
    )
    # Correctly extract the float embedding
    return response.embeddings.float[0]

def retrieve_relevant_chunks(user_query, top_k=2):
    """Retrieves the most relevant document chunks."""
    formatted_query = format_user_question(user_query)  # Apply query formatting
    query_embedding = get_embedding(formatted_query)

    # Initialize PGVector for retrieval
    connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    vector_store = PGVector(
        connection=connection_string,  # Pass the connection string
        embeddings=co,  # Pass the Cohere client
        collection_name="collection",  # Specify the collection name
    )

    # Perform similarity search
    results = vector_store.similarity_search_by_vector(query_embedding, k=top_k)

    responses = results[0].page_content 

    return responses