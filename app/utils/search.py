"""Search helpers for text normalization and partial matching."""

import re
from typing import Callable, Iterable, List, TypeVar

T = TypeVar("T")


def normalize(text: str) -> str:
    """Normalize text by collapsing whitespace and lowercasing."""
    return re.sub(r"\s+", " ", text).strip().lower()


def matches_query(items: Iterable[T], getter: Callable[[T], str], query: str | None) -> List[T]:
    """Return items whose getter value contains the normalized query as a substring."""
    if not query:
        return list(items)
    q = normalize(query)
    results: List[T] = []
    for item in items:
        value = normalize(getter(item))
        if q in value:
            results.append(item)
    return results
