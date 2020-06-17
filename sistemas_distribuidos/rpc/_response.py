# Standard
import typing as T


class Response(T.TypedDict):
    data: T.Any
    error: T.Optional[str]
