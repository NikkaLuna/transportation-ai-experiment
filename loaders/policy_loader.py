from langchain_core.documents import Document
from pathlib import Path
from typing import List

def load_policy_documents(policy_dir: str) -> List[Document]:
    docs = []

    for file_path in Path(policy_dir).glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        docs.append(
            Document(
                page_content=text,
                metadata={"source": file_path.name}
            )
        )

    if not docs:
        raise FileNotFoundError(f"No .txt policy files found in {policy_dir}")

    print(f"Loaded {len(docs)} policy document(s)")
    return docs