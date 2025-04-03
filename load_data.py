import os
import argparse

from chromadb import Settings
from tqdm import tqdm
import chromadb
from chromadb.utils import embedding_functions
import pypdf
from Env import Env


def main(
        documents_directory: str = "documents",
        collection_name: str = "documents_collection",
        persist_directory: str = ".",

) -> None:
    # Read all files in the data directory
    documents = []
    metadatas = []

    files = os.listdir(documents_directory)

    def add_line(line: str, filename: str, line_number: int):
        # Strip whitespace and append the line to the documents list
        line = line.strip()
        # Skip empty lines
        if len(line) == 0:
            return
        documents.append(line)
        metadatas.append({"filename": filename, "line_number": line_number})

    for filename in files:
        if filename.endswith(".pdf"):
            pdf = pypdf.PdfReader(f"{documents_directory}/{filename}")
            pages: int = 0
            for page in pdf.pages:
                pages += 1
                print(f"Page {pages}")
                text = page.extract_text()
                # Split by double newlines to separate paragraphs
                paragraphs = text.split('\n\n')
                print(len(paragraphs))
                # Remove empty paragraphs and clean up extra whitespace
                paragraphs = [p.strip() for p in paragraphs if p.strip()]
                for (line_number, paragraph) in enumerate(paragraphs):
                    print("paragraph ================")
                    print(paragraph)
                    print("paragraph ================")
                    add_line(line=paragraph, filename=filename, line_number=line_number)
        else:
            with open(f"{documents_directory}/{filename}", "r") as file:
                for line_number, line in enumerate(file.readlines()):
                    add_line(line=line, filename=filename, line_number=line_number)

    print(documents)

    # Instantiate a persistent chroma client in the persist_directory.
    # Learn more at docs.trychroma.com
    client = chromadb.PersistentClient(
        path=persist_directory,
        settings=Settings(
            allow_reset=True
        )
    )

    # Reset the client to clear previous data
    client.reset()

    google_api_key = Env("GEMINI_API_KEY")

    # create embedding function
    embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
        api_key=google_api_key
    )

    # If the collection already exists, we just return it. This allows us to add more
    # data to an existing collection.
    collection = client.get_or_create_collection(
        name=collection_name, embedding_function=embedding_function
    )

    # Create ids from the current count
    count = collection.count()
    print(f"Collection already contains {count} documents")
    ids = [str(i) for i in range(count, count + len(documents))]

    # Load the documents in batches of 100
    for i in tqdm(
            range(0, len(documents), 100), desc="Adding documents", unit_scale=100,
    ):
        collection.add(
            ids=ids[i: i + 100],
            documents=documents[i: i + 100],
            metadatas=metadatas[i: i + 100],  # type: ignore
        )

    new_count = collection.count()
    print(f"Added {new_count - count} documents")


if __name__ == "__main__":
    # Read the data directory, collection name, and persist directory
    parser = argparse.ArgumentParser(
        description="Load documents from a directory into a Chroma collection"
    )

    # Add arguments
    parser.add_argument(
        "--data_directory",
        type=str,
        default="documents",
        help="The directory where your text files are stored",
    )
    parser.add_argument(
        "--collection_name",
        type=str,
        default="documents_collection",
        help="The name of the Chroma collection",
    )
    parser.add_argument(
        "--persist_directory",
        type=str,
        default="chroma_storage",
        help="The directory where you want to store the Chroma collection",
    )

    # Parse arguments
    args = parser.parse_args()

    main(
        documents_directory=args.data_directory,
        collection_name=args.collection_name,
        persist_directory=args.persist_directory,
    )
