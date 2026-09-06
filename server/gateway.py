"""Clean-room HTTP bootstrap skeleton.

Exact Online/MMO response schemas are intentionally left unimplemented until
they are recovered from client behavior/native analysis.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class GatewayHandler(BaseHTTPRequestHandler):
    server_version = "DurangoPreservation/0.1"

    def do_GET(self):
        self.send_error(501, "Online bootstrap schema not implemented yet")

    def do_POST(self):
        self.send_error(501, "Online bootstrap schema not implemented yet")


def main(host: str = "127.0.0.1", port: int = 18081) -> None:
    server = ThreadingHTTPServer((host, port), GatewayHandler)
    print(f"Durango clean-room HTTP bootstrap: http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
