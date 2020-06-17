# Standard
import typing as T

# Project
from ..base import connect as _connect
from ._request import Request
from ._response import Response

client: T.Callable[[str, int], T.Generator[Response, Request, None]] = _connect
