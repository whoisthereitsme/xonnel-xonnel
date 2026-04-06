from __future__ import annotations

import json
import socket


HOST_SERVER = "192.168.0.104"
HOST_CLIENT = "192.168.0.25"
PORT = 12345


class XDbaseClient:
    def __init__(self, host: str = HOST_SERVER, port: int = PORT):
        self.host = host
        self.port = port

    def send(self, payload: dict):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # optional: bind explicitly to the sending machine IP
        sock.bind((HOST_CLIENT, 0))

        sock.connect((self.host, self.port))
        sock.sendall(json.dumps(payload).encode())
        data = sock.recv(1024 * 1024)
        sock.close()
        return json.loads(data.decode())

    def write(self, **kwargs):
        return self.send({
            "mode": "write",
            "data": kwargs,
        })

    def read(self, **kwargs):
        return self.send({
            "mode": "read",
            "query": kwargs,
        })


if __name__ == "__main__":
    client = XDbaseClient(host="192.168.0.104", port=12345)

    print(client.write(id=1, level="INFO", msg="hello from 192.168.0.25"))
    print(client.write(id=2, level="ERROR", msg="boom"))

    print(client.read())
    print(client.read(level="INFO"))