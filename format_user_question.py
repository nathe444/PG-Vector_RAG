import re
import string
import os


def format_user_question(user_query):
    """
    Formats the user query for processing by:
    1. Converting to lowercase.
    2. Removing punctuation.
    3. Trimming extra spaces.
    """
    # Convert to lowercase
    user_query = user_query.lower()

    # Remove punctuation
    user_query = user_query.translate(str.maketrans('', '', string.punctuation))

    # Trim extra spaces
    user_query = re.sub(r'\s+', ' ', user_query).strip()

    return user_query