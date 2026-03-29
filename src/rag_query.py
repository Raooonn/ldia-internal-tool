import re
import pandas as pd


CHUNKS_PATH = "data/chunks.csv"


def normalize_text(text):
    text = text.lower()
    words = re.findall(r"\b\w+\b", text)
    return words


def score_chunk(query_words, chunk_text):
    chunk_words = normalize_text(chunk_text)
    overlap = set(query_words) & set(chunk_words)
    return len(overlap), overlap


def search_chunks(query, top_k=3):
    df = pd.read_csv(CHUNKS_PATH)

    query_words = normalize_text(query)
    results = []

    for _, row in df.iterrows():
        score, overlap = score_chunk(query_words, row["chunk_text"])

        results.append(
            {
                "doc_name": row["doc_name"],
                "chunk_id": row["chunk_id"],
                "chunk_text": row["chunk_text"],
                "score": score,
                "overlap_words": ", ".join(sorted(overlap)),
            }
        )

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by="score", ascending=False)

    return results_df.head(top_k)


if __name__ == "__main__":
    query = input("Ask a question: ")
    top_results = search_chunks(query)

    print("\nTop matching chunks:\n")
    print(top_results[["doc_name", "chunk_id", "score", "overlap_words"]])

    print("\nBest chunk text:\n")
    if len(top_results) > 0:
        print(top_results.iloc[0]["chunk_text"])