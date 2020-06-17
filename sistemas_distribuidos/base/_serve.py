# Standard
from select import select
from socket import AF_INET, SOCK_STREAM, socket
from logging import getLogger
from contextlib import ExitStack, suppress
from collections import defaultdict
import json
import typing as T

logger: T.Final = getLogger(__name__)


def serve(host: str, port: int) -> T.Generator[T.Any, T.Any, None]:
    read: T.Final[T.MutableMapping[socket, bytearray]] = {}
    write: T.Final[T.MutableMapping[socket, bytearray]] = defaultdict(bytearray)

    def close_connection(conn: socket) -> None:
        try:
            peer_name = conn.getpeername()
        except OSError:
            peer_name = "unknown"

        read.pop(conn)
        if conn in write:
            write.pop(conn)

        with suppress(OSError):
            conn.close()

        logger.warning("Closed connection to %s", peer_name)

    with ExitStack() as stack:
        # Create server socket
        server: T.Final[socket] = stack.enter_context(socket(family=AF_INET, type=SOCK_STREAM))

        @stack.callback
        def close_connections() -> None:
            for conn in tuple(read):
                close_connection(conn)

        # Enable unblocking mode
        server.setblocking(False)

        # Bind it to interface and port
        server.bind((host, port))

        # Listen for incoming client connections
        server.listen()

        logger.info(f"Server initialized at (%s, %d)", host, port)

        # Server connection loop
        read[server] = bytearray()
        while read:
            readable: T.List[socket]
            writable: T.List[socket]
            exceptional: T.List[socket]
            # Wait for any socket availability for reading or writing
            readable, writable, exceptional = select(read, write, read)

            for connection in readable:
                if connection.fileno() == -1:
                    continue

                if connection is server:
                    # A client established a connection
                    connection, client_address = connection.accept()
                    connection.setblocking(False)
                    read[connection] = bytearray()
                    logger.info(f"Opened connection to %s", client_address)
                else:
                    # Received a message from a client connection
                    try:
                        buffer = read[connection]
                        if data := connection.recv(1024):
                            buffer += data
                            messages = buffer.split(b"\n")
                            buffer = messages.pop()
                            for msg in messages:
                                logger.debug(
                                    "Received message from connection at %s: %s",
                                    connection.getpeername(),
                                    msg,
                                )
                                to_write = yield json.loads(msg)
                                if to_write is None:
                                    close_connection(connection)
                                else:
                                    write[connection] += (
                                        bytes(json.dumps(to_write), encoding="utf8") + b"\n"
                                    )
                            read[connection] = buffer
                        else:
                            close_connection(connection)
                    except Exception as exc:
                        logger.error(exc)
                        close_connection(connection)

            for connection in writable:
                if connection.fileno() == -1:
                    continue

                if buffer := write[connection]:
                    # Write any pending message to the relative client connection
                    try:
                        written_bytes = connection.send(buffer)
                        msg = buffer[:written_bytes]
                        write[connection] = buffer[written_bytes:]
                    except Exception as exc:
                        logger.error(exc)
                        close_connection(connection)
                    else:
                        logger.debug(
                            "Sent message to connection at %s: %s", connection.getpeername(), msg
                        )

            for connection in exceptional:
                if connection.fileno() == -1:
                    continue

                # Close any connection that is in exceptional state
                close_connection(connection)
