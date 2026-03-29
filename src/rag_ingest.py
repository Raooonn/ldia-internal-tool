from pathlib import Path
import pandas as pd


DOCS_PATH = Path("docs")
OUTPUT_PATH = Path("data/chunks.csv")


def chunk_text(text, chunk_size=500):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end

    return chunks


def build_chunks():
    rows = []

    for file_path in DOCS_PATH.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks, start=1):
            rows.append(
                {
                    "doc_name": file_path.name,
                    "chunk_id": i,
                    "chunk_text": chunk,
                }
            )

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_PATH, index=False)
    return df


if __name__ == "__main__":
    df = build_chunks()
    print("RAG ingest completed.")
    print(f"Total chunks created: {len(df)}")
    print(df[["doc_name", "chunk_id"]])