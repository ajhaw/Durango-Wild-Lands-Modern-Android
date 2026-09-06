"""Clean-room TCP frontend skeleton."""

import socket
from .protocol import HEADER_SIZE, PacketHeader


def recv_exact(sock: socket.socket, size: int) -> bytes:
    data = bytearray()
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise EOFError("client disconnected")
        data.extend(chunk)
    return bytes(data)


def handle_client(client: socket.socket, address) -> None:
    print(f"TCP client connected: {address}")
    try:
        while True:
            raw_header = recv_exact(client, HEADER_SIZE)
            header = PacketHeader.unpack(raw_header)
            payload = recv_exact(client, header.payload_size)
            print(
                f"type={header.type_code} seq={header.seq} "
                f"reply_of={header.reply_of} compressed={len(payload)}"
            )
            # TODO: raw Snappy decode + MessagePack dispatch.
    except EOFError:
        pass
    finally:
        client.close()
        print(f"TCP client disconnected: {address}")


def main(host: str = "127.0.0.1", port: int = 18191) -> None:
    with socket.create_server((host, port)) as server:
        print(f"Durango clean-room TCP frontend: {host}:{port}")
        while True:
            client, address = server.accept()
            handle_client(client, address)


if __name__ == "__main__":
    main()
