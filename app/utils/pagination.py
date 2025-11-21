from typing import List, Sequence, Tuple, TypeVar

from app.models.pagination_model import PaginationMeta

T = TypeVar("T")


def paginate_items(items: Sequence[T], page: int, size: int) -> Tuple[List[T], PaginationMeta]:
    start = (page - 1) * size
    end = start + size
    sliced = list(items[start:end])
    meta = PaginationMeta.from_counts(page=page, size=size, total_items=len(items))
    return sliced, meta
