from typing import List, Sequence, Tuple, TypeVar

from app.models import PaginationMetaModel

T = TypeVar("T")


def paginate_items(items: Sequence[T], page: int, size: int) -> Tuple[List[T], PaginationMetaModel]:
    """Slice a list/sequence and build pagination metadata."""
    start = (page - 1) * size
    end = start + size
    sliced = list(items[start:end])
    meta = PaginationMetaModel.from_counts(page=page, size=size, total_items=len(items))
    return sliced, meta
