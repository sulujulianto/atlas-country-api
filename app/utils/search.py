import re
from typing import Callable, Iterable, List, TypeVar

T = TypeVar("T")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def matches_query(items: Iterable[T], getter: Callable[[T], str], query: str | None) -> List[T]:
    if not query:
        return list(items)
    q = normalize(query)
    results: List[T] = []
    for item in items:
        value = normalize(getter(item))
        if q in value:
            results.append(item)
    return results
