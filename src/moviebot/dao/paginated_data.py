from typing import Callable, List, Generic, TypeVar

T = TypeVar("T")


class PaginatedData(Generic[T]):
    def __init__(
        self,
        data: List[T],
        offset: int,
        limit: int,
        total: int,
        paginate: Callable[[int, int], "PaginatedData[T]"],
    ):
        self.data = data
        self.offset = offset
        self.limit = limit
        self.total = total
        self.paginate = paginate

    def next_page_exists(self) -> bool:
        return self.offset + self.limit < self.total

    def previous_page_exists(self) -> bool:
        return self.offset > 0

    def get_next_page(self) -> "PaginatedData[T]":
        return self.paginate(self.offset + self.limit, self.limit)

    def get_previous_page(self) -> "PaginatedData[T]":
        return self.paginate(max(0, self.offset - self.limit), self.limit)

    def get_first_page(self) -> "PaginatedData[T]":
        return self.paginate(0, self.limit)

    def get_last_page(self) -> "PaginatedData[T]":
        return self.paginate(self.total - self.limit, self.limit)
