"""Filtering helpers for numeric ranges, region/subregion, and list membership."""

from typing import Callable, Iterable, List, TypeVar

T = TypeVar("T")


def apply_numeric_filter(
    items: Iterable[T],
    getter: Callable[[T], float | int],
    min_value: float | int | None,
    max_value: float | int | None,
) -> List[T]:
    """Filter items by numeric min/max bounds using a getter."""
    results: List[T] = []
    for item in items:
        value = getter(item)
        if min_value is not None and value < min_value:
            continue
        if max_value is not None and value > max_value:
            continue
        results.append(item)
    return results


def filter_by_region(
    items: Iterable[T],
    region_getter: Callable[[T], str],
    region: str | None,
    subregion_getter: Callable[[T], str] | None = None,
    subregion: str | None = None,
) -> List[T]:
    """Filter items by region/subregion (case-insensitive)."""
    results: List[T] = []
    for item in items:
        region_val = region_getter(item)
        if region and region_val.lower() != region.lower():
            continue
        if subregion and subregion_getter:
            if subregion_getter(item).lower() != subregion.lower():
                continue
        results.append(item)
    return results


def filter_by_list_field(items: Iterable[T], getter: Callable[[T], list[str]], value: str | None) -> List[T]:
    """Filter items where a list field contains a case-insensitive value."""
    if not value:
        return list(items)
    value_lower = value.lower()
    results: List[T] = []
    for item in items:
        values = getter(item)
        if any(value_lower == v.lower() for v in values):
            results.append(item)
    return results
