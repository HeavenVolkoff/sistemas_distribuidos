# Standard
import typing as T

# External
import click

# Project
from ..base import connect


@click.command()
@click.option(
    "--host",
    "-h",
    type=str,
    default="localhost",
    help="Address for the host serving the hello server.",
)
@click.option(
    "--port",
    "-p",
    type=int,
    default=5678,
    help="Port where the hello server is available in the remote host.",
)
def client(host: str = "localhost", port: int = 5678) -> T.NoReturn:
    """Hello client."""
    connection = connect(host, port)

    try:
        connection.send(None)
        print(connection.send("hello"))
    except StopIteration:
        pass

    exit(0)


if __name__ == "__main__":
    client()
