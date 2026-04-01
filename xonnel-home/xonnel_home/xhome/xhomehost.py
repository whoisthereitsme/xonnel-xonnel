# xhomehost.py

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import json
import socket
import struct
import threading
from pathlib import Path


class XHomeHostClient:
    def __init__(self, host=None, conn: socket.socket = None, addr=None):
        self.host = host
        self.conn = conn
        self.addr = addr

    def handle(self):
        try:
            meta = self.recv_meta()
            cmd = meta.get("cmd")
            path = meta.get("path")

            if cmd == "save":
                data = self.recv_data()
                self.host.save(path=path, data=data)
                self.send_meta({
                    "ok": True,
                    "cmd": "save",
                    "path": Path(path).as_posix(),
                    "size": len(data),
                })
                return

            if cmd == "load":
                data = self.host.load(path=path)
                self.send_meta({
                    "ok": True,
                    "cmd": "load",
                    "path": Path(path).as_posix(),
                    "size": len(data),
                })
                self.send_data(data=data)
                return

            self.send_meta({
                "ok": False,
                "error": f"[ERROR] [XHomeHostClient.handle()] Unknown command: {cmd}",
            })

        except Exception as e:
            try:
                self.send_meta({
                    "ok": False,
                    "error": str(e),
                })
            except Exception:
                ...
        finally:
            try:
                self.conn.close()
            except Exception:
                ...

    def recv_meta(self):
        size = struct.unpack("!Q", self.recv_exact(8))[0]
        if size == 0:
            return {}

        raw = self.recv_exact(size)
        return json.loads(raw.decode("utf-8"))

    def send_meta(self, data: dict = None):
        if data is None:
            data = {}
        if not isinstance(data, dict):
            raise TypeError("[ERROR] [XHomeHostClient.send_meta()] Meta must be dict.")

        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.conn.sendall(struct.pack("!Q", len(raw)))
        if raw:
            self.conn.sendall(raw)

    def recv_data(self):
        size = struct.unpack("!Q", self.recv_exact(8))[0]
        if size == 0:
            return b""
        return self.recv_exact(size)

    def send_data(self, data: bytes = None):
        if data is None:
            data = b""
        if not isinstance(data, bytes):
            raise TypeError("[ERROR] [XHomeHostClient.send_data()] Data must be bytes.")

        self.conn.sendall(struct.pack("!Q", len(data)))
        if data:
            self.conn.sendall(data)

    def recv_exact(self, size: int = None):
        if size is None or size < 0:
            raise ValueError("[ERROR] [XHomeHostClient.recv_exact()] Invalid size.")

        data = bytearray()
        while len(data) < size:
            chunk = self.conn.recv(size - len(data))
            if not chunk:
                raise ConnectionError("[ERROR] [XHomeHostClient.recv_exact()] Socket closed while receiving data.")
            data.extend(chunk)
        return bytes(data)


class XHomeHost:
    def __init__(self, host: str = None, port: int = None, timeout: float = 30.0):
        self.host = host
        self.port = port
        self.timeout = timeout

        self.sock = None
        self.running = False
        self.thread = None

        self.start()

    def start(self):
        if self.running:
            return self

        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()
        return self

    def stop(self):
        self.running = False

        try:
            if self.sock is not None:
                self.sock.close()
        except Exception:
            ...

        return self

    def save(self, path: str | Path = None, data: bytes = None):
        if path is None:
            raise ValueError("[ERROR] [XHomeHost.save()] No path provided.")
        if data is None:
            data = b""
        if not isinstance(data, bytes):
            raise TypeError("[ERROR] [XHomeHost.save()] Data must be bytes.")

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def load(self, path: str | Path = None):
        if path is None:
            raise ValueError("[ERROR] [XHomeHost.load()] No path provided.")

        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"[ERROR] [XHomeHost.load()] File not found: {path}")
        if not path.is_file():
            raise IsADirectoryError(f"[ERROR] [XHomeHost.load()] Path is not a file: {path}")

        return path.read_bytes()

    def _loop(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen()

        while self.running:
            try:
                conn, addr = self.sock.accept()
                client = XHomeHostClient(host=self, conn=conn, addr=addr)
                threading.Thread(target=client.handle, daemon=True).start()
            except OSError:
                break
            except Exception:
                ...