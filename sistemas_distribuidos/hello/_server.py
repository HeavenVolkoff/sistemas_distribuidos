# External
import click

# Project
from ..base import serve


@click.command()
@click.argument("host", type=str)
@click.argument("port", type=int)
def server(host: str, port: int) -> None:
    """Hello server.

    HOST is the interface address which will be used to expose the hello server.
    PORT is the port which will be used to accept connection to the hello server.

    """
    response = None
    connection = serve(host, port)
    while True:
        try:
            connection.send(response)
            response = "Hello"
        except StopIteration:
            break


if __name__ == "__main__":
    server()
