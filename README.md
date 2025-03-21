# Chat with your documents

This project contains a (very) minimal, self-contained example of how to add your custom documents to gemini to extend its knowledge base, using Chroma and Google Gemini's API.
It uses fictional hybird car article as example document.

## How it works

The basic flow is as follows:

0. The text documents in the `documents` folder are loaded line by line, then embedded and stored in a Chroma collection.

1. When the user submits a question, it gets embedded using the same model as the documents, and the lines most relevant to the query are retrieved by Chroma.
2. The user-submitted question is passed to Google Gemini's API, along with the extra context retrieved by Chroma. The Google Gemini API generates a response.
3. The response is displayed to the user, along with the lines used as extra context.

## Running the example

You will need an Gemini API key to run this demo.

Install dependencies and run the example:

```bash
# 1- Install dependencies
pip install -r requirements.txt

# 2- Load the example documents into Chroma
python load_data.py

# 3- Set your GEMINI_API_KEY environment variable to .env

# 4- Run gemini
python main.py
```

Example output:

```
Query: What is starlight queen?

Thinking...

Based on the information provided, "Starlight Queen" refers to a hybrid vehicle. It is the latest offering from Stellar Motors. It's described as a luxurious and fuel-efficient hybrid with a smooth ride and responsive handling. It is considered a premium vehicle due to its high price tag.



Source documents:
StarlightQueen.md: line 19
StarlightQueen.md: line 33
StarlightQueen.md: line 1
StarlightQueen.md: line 31
StarlightQueen.md: line 5
```

You can replace the example text documents in the `documents` folder with your own documents, and the chatbot will use those instead.