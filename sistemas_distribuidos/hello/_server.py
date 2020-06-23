# Standard
import typing as T

# External
import click

# Project
from ..base import serve


@click.command()
@click.option(
    "--host",
    "-h",
    type=str,
    default="localhost",
    help="Interface address which will be used to expose the hello server",
)
@click.option(
    "--port",
    "-p",
    type=int,
    default=5678,
    help="Port which will be used to accept connection to the hello server",
)
def server(host: str = "localhost", port: int = 5678) -> T.NoReturn:
    """Hello server."""
    response = None
    connection = serve(host, port)
    while True:
        try:
            connection.send(response)
            response = "Hello"
        except StopIteration:
            break
    exit(0)


if __name__ == "__main__":
    server()
