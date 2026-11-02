from openai import OpenAI


def build_context(retrieved_chunks: list[dict]) -> str:
    parts = []
    for item in retrieved_chunks:
        parts.append(
            f"Chunk {item['chunk_id']} from {item['source']}\n"
            f"Similarity score: {item['score']:.4f}\n"
            f"{item['text']}"
        )
    return "\n\n".join(parts)


def answer_question(
    client: OpenAI, question: str, retrieved_chunks: list[dict], model: str
) -> str:
    context = build_context(retrieved_chunks)

    system_prompt = (
        "You answer questions only from the provided PDF context. "
        "If the answer is not in the context, say that clearly."
    )

    user_prompt = (
        f"Question:\n{question}\n\n"
        f"Context from the PDF:\n{context}\n\n"
        "Answer in 2 to 4 short sentences using only the context above. If the answer is not in the context, say that clearly."
    )

    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.output_text
