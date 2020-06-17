# External
import click

# Project
from . import exposed
from .. import rpc


@click.command()
@click.argument("host", type=str)
@click.argument("port", type=int)
def server(host: str, port: int) -> None:
    """Remote calculator server.

    HOST is the interface address which will be used to expose the hello server.
    PORT is the port which will be used to accept connection to the hello server.

    """
    rpc.server(host, port, {name: func for name, func in vars(exposed).items() if callable(func)})


if __name__ == "__main__":
    server()
