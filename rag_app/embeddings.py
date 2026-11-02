from openai import OpenAI


def create_embedding(client: OpenAI, text: str, model: str) -> list[float]:
    """Create one embedding vector for one text chunk."""
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding
