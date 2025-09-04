from typing import List, Dict
from whoosh.fields import Schema, TEXT, ID
from whoosh import index
from whoosh.qparser import MultifieldParser
from whoosh.analysis import StemmingAnalyzer
import os
import shutil


ANALYZER = StemmingAnalyzer()


def get_schema() -> Schema:
    return Schema(
        id=ID(stored=True, unique=True),
        title=TEXT(stored=True, analyzer=ANALYZER),
        body=TEXT(stored=True, analyzer=ANALYZER),
        tags=TEXT(stored=True, analyzer=ANALYZER),
        doc_types=TEXT(stored=True, analyzer=ANALYZER),
        jurisdictions=TEXT(stored=True, analyzer=ANALYZER),
    )


def build_index(index_dir: str, clauses: List[Dict]) -> None:
    if os.path.isdir(index_dir):
        shutil.rmtree(index_dir)
    os.makedirs(index_dir, exist_ok=True)
    ix = index.create_in(index_dir, get_schema())
    writer = ix.writer()
    for c in clauses:
        writer.add_document(
            id=c["id"],
            title=c.get("title", ""),
            body=c.get("body", ""),
            tags=" ".join(c.get("tags", [])),
            doc_types=" ".join(c.get("doc_types", [])),
            jurisdictions=" ".join(c.get("jurisdictions", [])),
        )
    writer.commit()


def query_index(index_dir: str, query: str, limit: int = 20):
    if not os.path.isdir(index_dir):
        return []
    ix = index.open_dir(index_dir)
    with ix.searcher() as searcher:
        parser = MultifieldParser(["title", "body", "tags"], schema=ix.schema)
        q = parser.parse(query or "")
        results = searcher.search(q, limit=limit)
        return [
            {
                "id": r["id"],
                "title": r.get("title", ""),
                "snippet": (r.get("body", "")[:180] + ("..." if len(r.get("body", "")) > 180 else "")),
                "score": float(r.score),
            }
            for r in results
        ]

