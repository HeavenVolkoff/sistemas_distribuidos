# Standard
import typing as T

# Project
from ..base import serve
from ._request import Request
from ._response import Response


def server(host: str, port: int, functions: T.Mapping[str, T.Callable[..., T.Any]]) -> None:
    response: T.Optional[Response] = None
    connection = serve(host, port)

    while True:
        try:
            request: Request = connection.send(response)
        except StopIteration:
            break

        data = None
        name = request["name"]
        error = None
        if name not in functions:
            error = f"Remote function<{name}> is not available"
        else:
            function = functions[name]
            arguments = request["args"]
            try:
                if isinstance(arguments, T.List):
                    data = function(*arguments)
                elif isinstance(arguments, T.Mapping):
                    data = function(**arguments)
                else:
                    raise TypeError("Invalid arguments")
            except Exception as exc:
                error = str(exc)

        response = {"data": data, "error": error}
