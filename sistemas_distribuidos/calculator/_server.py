# Standard
import typing as T

# External
import click

# Project
from . import exposed
from .. import rpc


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
    """Remote calculator server."""
    rpc.server(host, port, {name: func for name, func in vars(exposed).items() if callable(func)})
    exit(0)


if __name__ == "__main__":
    server()
