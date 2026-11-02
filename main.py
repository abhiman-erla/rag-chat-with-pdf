from pathlib import Path

from openai import OpenAI

from rag_app.chunking import split_text_into_chunks
from rag_app.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    CHUNK_STORE_PATH,
    EMBEDDING_MODEL,
    PDF_DIR,
    TOP_K,
    CHAT_MODEL,
    load_settings,
)
from rag_app.embeddings import create_embedding
from rag_app.pdf_utils import extract_text_from_pdf
from rag_app.qa import answer_question
from rag_app.vector_store import load_chunks, save_chunks, search_similar_chunks


def ingest_pdf(client: OpenAI, pdf_path: Path) -> None:
    print(f"\nReading PDF: {pdf_path.name}")
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        raise ValueError("No readable text was found in the PDF.")

    chunks = split_text_into_chunks(text, CHUNK_SIZE, CHUNK_OVERLAP)
    if not chunks:
        raise ValueError("Chunking produced no chunks.")

    print(f"Created {len(chunks)} chunks. Creating embeddings...")

    records = []
    for index, chunk in enumerate(chunks, start=1):
        embedding = create_embedding(client, chunk, EMBEDDING_MODEL)
        records.append(
            {
                "chunk_id": index,
                "source": pdf_path.name,
                "text": chunk,
                "embedding": embedding,
            }
        )

    save_chunks(CHUNK_STORE_PATH, records)
    print(f"Saved chunk store to: {CHUNK_STORE_PATH}")


def ask_question(client: OpenAI) -> None:
    records = load_chunks(CHUNK_STORE_PATH)
    if not records:
        raise ValueError("No chunk store found. Ingest a PDF first.")

    question = input("\nAsk a question about the PDF: ").strip()
    if not question:
        raise ValueError("Question cannot be empty.")

    query_embedding = create_embedding(client, question, EMBEDDING_MODEL)
    retrieved = search_similar_chunks(query_embedding, records, TOP_K)

    print("\nTop retrieved chunks:")
    for item in retrieved:
        preview = item["text"][:140].replace("\n", " ")
        print(f"- Chunk {item['chunk_id']} | score={item['score']:.4f} | {preview}...")

    answer = answer_question(client, question, retrieved, CHAT_MODEL)
    print("\nAnswer:\n")
    print(answer)


def pick_pdf() -> Path:
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF found. Put one PDF inside this folder: {PDF_DIR}"
        )

    if len(pdf_files) == 1:
        return pdf_files[0]

    print("Multiple PDFs found:")
    for index, pdf in enumerate(pdf_files, start=1):
        print(f"{index}. {pdf.name}")

    choice = input("Choose a PDF number: ").strip()
    if not choice.isdigit():
        raise ValueError("Please enter a valid number.")

    selected_index = int(choice) - 1
    if selected_index < 0 or selected_index >= len(pdf_files):
        raise ValueError("That PDF number is out of range.")

    return pdf_files[selected_index]


def main() -> None:
    api_key = load_settings()
    client = OpenAI(api_key=api_key)

    print("Level 1 RAG: Chat with PDF")
    print("1. Ingest PDF")
    print("2. Ask a question")
    choice = input("Choose an option (1 or 2): ").strip()

    if choice == "1":
        pdf_path = pick_pdf()
        ingest_pdf(client, pdf_path)
    elif choice == "2":
        ask_question(client)
    else:
        print("Please choose 1 or 2.")


if __name__ == "__main__":
    main()
