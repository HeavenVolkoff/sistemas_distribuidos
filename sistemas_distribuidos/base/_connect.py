# Standard
from socket import AF_INET, SOCK_STREAM, socket
from contextlib import ExitStack
import json
import typing as T


def connect(host: str, port: int) -> T.Generator[T.Any, T.Any, None]:
    with ExitStack() as stack:
        buffer = bytearray()
        # Create client socket
        connection: T.Final[socket] = stack.enter_context(socket(family=AF_INET, type=SOCK_STREAM))
        # Open connection to server
        connection.connect((host, port))

        # Client connection loop
        msg = yield
        while msg is not None:
            connection.sendall(bytes(json.dumps(msg), encoding="utf8") + b"\n")
            while len(messages := buffer.split(b"\n")) == 1:
                if msg := connection.recv(1024):
                    buffer += msg
                else:
                    return
            msg, buffer = messages
            msg = yield json.loads(msg)
