import json

import chromadb
from chromadb.utils import embedding_functions

from Env import Env

google_api_key = Env("GEMINI_API_KEY")

# Instantiate a persistent chroma client in the persist_directory.
# This will automatically load any previously saved collections.
# Learn more at docs.trychroma.com
client = chromadb.PersistentClient(path="chroma_storage")

# create embedding function
embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
    api_key=google_api_key, task_type="RETRIEVAL_QUERY"
)

# Get the collection.
collection = client.get_collection(
    name="documents_collection", embedding_function=embedding_function
)

results = collection.query(
    query_texts=["Stellar Motors"],
    n_results=5,
    include=["documents", "metadatas"]
)

print("DOCUMENTS: =========================")
print(results["documents"])
print("ALL DATA: =========================")
print(json.dumps(results, indent=2, default=str))
