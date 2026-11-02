# Chat with PDF: A Minimal RAG App

This is Level 1 of a Retrieval-Augmented Generation (RAG) project.

The goal is to learn the core RAG pipeline with the smallest possible app:

1. Load one PDF
2. Read its text
3. Split the text into chunks
4. Turn each chunk into an embedding
5. Store those chunks and embeddings
6. Ask a question
7. Retrieve the most relevant chunks
8. Generate an answer using only those chunks

## Why this is a good first RAG project

This teaches the full base of RAG without adding extra complexity like:

- web scraping
- databases
- UI frameworks
- authentication
- background jobs

You still learn the important ideas:

- ingestion
- chunking
- embeddings
- vector similarity
- retrieval
- grounded answer generation

## Project structure

```text
rag-chat-with-pdf/
|-- .env
|-- main.py
|-- requirements.txt
|-- data/
|   |-- pdfs/
|   |-- store/
|-- rag_app/
|   |-- __init__.py
|   |-- chunking.py
|   |-- config.py
|   |-- embeddings.py
|   |-- pdf_utils.py
|   |-- qa.py
|   |-- vector_store.py
```

## Setup

Activate your virtual environment first.

### cmd

```cmd
cd /d g:\vscode\codes\rag_1_E
.venv\Scripts\activate
```

Install dependencies if needed:

```cmd
pip install -r requirements.txt
```

## Add a PDF

Create these folders if they do not exist:

```cmd
mkdir data
mkdir data\pdfs
mkdir data\store
```

Put one PDF file inside `data\pdfs`.

Example:

```text
data/pdfs/my_document.pdf
```

## Run the app

```cmd
python main.py
```

You will see:

```text
Level 1 RAG: Chat with PDF
1. Ingest PDF
2. Ask a question
```

### Step 1: ingest the PDF

Choose `1`.

What happens:

- the PDF is opened
- text is extracted from each page
- text is split into overlapping chunks
- embeddings are created for each chunk
- the chunks are saved to `data/store/chunks.json`

### Step 2: ask a question

Run the app again and choose `2`.

What happens:

- your question is converted into an embedding
- the app compares your question vector with stored chunk vectors
- the top matching chunks are retrieved
- those chunks are sent to the model as context
- the model answers only from that context

## Detailed explanation of each part

## 1. PDF reading

This happens in `rag_app/pdf_utils.py`.

We use `pypdf` to extract text page by page.

Why page by page matters:

- PDFs are structured as pages
- some pages may be empty or image-only
- adding page markers makes debugging easier

## 2. Chunking

This happens in `rag_app/chunking.py`.

Large documents are too big to send directly to the model every time, so we split them into smaller parts called chunks.

Why chunking matters:

- embeddings work on manageable pieces of text
- retrieval becomes more precise
- prompt size stays small

Why overlap matters:

- sometimes a useful sentence sits at the edge of a chunk
- overlap lets nearby chunks share some context
- this reduces information loss

## 3. Embeddings

This happens in `rag_app/embeddings.py`.

An embedding is a list of numbers that represents the meaning of a text.

We embed:

- every chunk during ingestion
- the user question during retrieval

Why:

- similar meanings produce similar vectors
- that allows semantic search, not just keyword matching

## 4. Storage

This happens in `rag_app/vector_store.py`.

For Level 1, we keep storage simple by using a JSON file.

Each stored record contains:

- chunk id
- source PDF name
- chunk text
- embedding vector

Why this is enough for now:

- you can inspect it easily
- it avoids database complexity
- it helps you understand what is actually being stored

Later, we can upgrade this to:

- FAISS
- Chroma
- PostgreSQL with pgvector

## 5. Retrieval

Also in `rag_app/vector_store.py`.

We compare the question embedding against every chunk embedding using cosine similarity.

Cosine similarity answers:

"How similar is the direction of these two vectors?"

High score means:

- the question and chunk likely talk about similar meaning

Then we sort by score and keep the top `k` chunks.

## 6. Answer generation

This happens in `rag_app/qa.py`.

We send the retrieved chunks to the chat model with a strict instruction:

- answer only from the provided context
- if the answer is missing, say so clearly

This is the "generation" part of RAG.

Retrieval gives the evidence.
Generation turns that evidence into a natural answer.

## Important limitation in Level 1

This project is intentionally basic.

It does not yet handle:

- scanned PDFs with no extractable text
- multiple documents in one shared index
- citations by exact page span
- chat history
- streaming responses
- web UI
- reranking
- metadata filters

That is fine.
This level is only for understanding the main flow.

## Suggested learning path after this

After Level 1 works, the best upgrades are:

1. Better chunking
2. Support multiple PDFs
3. Add citations with page numbers
4. Use a real vector database
5. Add a simple Streamlit UI
6. Add conversation memory

## Quick test flow

1. Put a PDF in `data/pdfs`
2. Run `python main.py`
3. Choose `1` to ingest
4. Run `python main.py` again
5. Choose `2` to ask a question

Example questions:

- "What is the main topic of this PDF?"
- "Summarize the first section."
- "What does the document say about pricing?"

## One important mindset

This is not "chatting with the model alone."

This is:

- retrieve relevant document pieces first
- then ask the model to answer from those pieces

That is the core idea of RAG.
