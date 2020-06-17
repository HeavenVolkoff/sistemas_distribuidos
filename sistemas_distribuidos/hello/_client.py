# External
import click

# Project
from ..base import connect


@click.command()
@click.argument("host", type=str)
@click.argument("port", type=int)
def client(host: str, port: int) -> None:
    """Hello client.

    HOST is the address for the host serving the hello server.
    PORT is the port where the hello server is available in the remote host.

    """
    connection = connect(host, port)

    try:
        connection.send(None)
        print(connection.send("hello"))
    except StopIteration:
        pass


if __name__ == "__main__":
    client()
