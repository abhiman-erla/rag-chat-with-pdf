





















def split_text_into_chunks(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    Split text into overlapping chunks.

    Why overlap exists:
    if a useful sentence lands at the edge of one chunk, overlap gives the next
    chunk some of that same context so retrieval does not lose it.
    """
    if not text.strip():
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == text_length:
            break
        start = max(end - overlap, 0)

    return chunks
