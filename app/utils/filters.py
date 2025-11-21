from typing import Callable, Iterable, List, TypeVar

T = TypeVar("T")


def apply_numeric_filter(
    items: Iterable[T],
    getter: Callable[[T], float | int],
    min_value: float | int | None,
    max_value: float | int | None,
) -> List[T]:
    results: List[T] = []
    for item in items:
        value = getter(item)
        if min_value is not None and value < min_value:
            continue
        if max_value is not None and value > max_value:
            continue
        results.append(item)
    return results


def filter_by_region(items: Iterable[T], getter: Callable[[T], str], region: str | None, subregion: str | None) -> List[T]:
    results: List[T] = []
    for item in items:
        region_val = getter(item)
        region_lower = region_val.lower()
        if region and region_lower != region.lower():
            continue
        if subregion:
            # subregion passed as separate getter? For now assume getter returns region for region, subregion checked externally.
            pass
        results.append(item)
    return results


def filter_by_list_field(items: Iterable[T], getter: Callable[[T], list[str]], value: str | None) -> List[T]:
    if not value:
        return list(items)
    value_lower = value.lower()
    results: List[T] = []
    for item in items:
        values = getter(item)
        if any(value_lower == v.lower() for v in values):
            results.append(item)
    return results
