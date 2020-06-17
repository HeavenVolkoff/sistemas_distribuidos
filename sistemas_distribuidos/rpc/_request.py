# Standard
import typing as T


class Request(T.TypedDict):
    name: str
    args: T.Union[T.Sequence[T.Any], T.Mapping[str, T.Any]]
