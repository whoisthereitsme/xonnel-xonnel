# xhomepeer.py

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import json
import socket
import struct
from pathlib import Path


class XHomePeer:
    def __init__(self, host: str = None, port: int = None, timeout: float = 30.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None

    def push(self, src: str | Path = None, tgt: str | Path = None):
        if src is None:
            raise ValueError("[ERROR] [XHomePeer.push()] No source path provided.")

        src = Path(src)
        tgt = src if tgt is None else Path(tgt)

        if not src.exists():
            raise FileNotFoundError(f"[ERROR] [XHomePeer.push()] File not found: {src}")
        if not src.is_file():
            raise IsADirectoryError(f"[ERROR] [XHomePeer.push()] Path is not a file: {src}")

        data = src.read_bytes()

        try:
            self.connect()
            self.send_meta({
                "cmd": "save",
                "path": tgt.as_posix(),
                "size": len(data),
            })
            self.send_data(data=data)

            reply = self.recv_meta()
            if not reply.get("ok", False):
                raise RuntimeError(reply.get("error", "[ERROR] [XHomePeer.push()] Push failed."))

            return {
                "ok": True,
                "cmd": "push",
                "src": src.as_posix(),
                "tgt": tgt.as_posix(),
                "size": len(data),
            }
        finally:
            self.close()

    def pull(self, src: str | Path = None, tgt: str | Path = None):
        if src is None:
            raise ValueError("[ERROR] [XHomePeer.pull()] No source path provided.")

        src = Path(src)
        tgt = src if tgt is None else Path(tgt)

        try:
            self.connect()
            self.send_meta({
                "cmd": "load",
                "path": src.as_posix(),
            })

            reply = self.recv_meta()
            if not reply.get("ok", False):
                raise RuntimeError(reply.get("error", "[ERROR] [XHomePeer.pull()] Pull failed."))

            data = self.recv_data()
        finally:
            self.close()

        tgt.parent.mkdir(parents=True, exist_ok=True)
        tgt.write_bytes(data)

        return {
            "ok": True,
            "cmd": "pull",
            "src": src.as_posix(),
            "tgt": tgt.as_posix(),
            "size": len(data),
        }

    def connect(self):
        self.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))
        return self

    def close(self):
        try:
            if self.sock is not None:
                self.sock.close()
        except Exception:
            ...
        finally:
            self.sock = None
        return self

    def send_meta(self, data: dict = None):
        if self.sock is None:
            raise ValueError("[ERROR] [XHomePeer.send_meta()] No socket connected.")
        if data is None:
            data = {}
        if not isinstance(data, dict):
            raise TypeError("[ERROR] [XHomePeer.send_meta()] Meta must be dict.")

        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.sock.sendall(struct.pack("!Q", len(raw)))
        if raw:
            self.sock.sendall(raw)

    def recv_meta(self):
        if self.sock is None:
            raise ValueError("[ERROR] [XHomePeer.recv_meta()] No socket connected.")

        size = struct.unpack("!Q", self.recv_exact(8))[0]
        if size == 0:
            return {}

        raw = self.recv_exact(size)
        return json.loads(raw.decode("utf-8"))

    def send_data(self, data: bytes = None):
        if self.sock is None:
            raise ValueError("[ERROR] [XHomePeer.send_data()] No socket connected.")
        if data is None:
            data = b""
        if not isinstance(data, bytes):
            raise TypeError("[ERROR] [XHomePeer.send_data()] Data must be bytes.")

        self.sock.sendall(struct.pack("!Q", len(data)))
        if data:
            self.sock.sendall(data)

    def recv_data(self):
        if self.sock is None:
            raise ValueError("[ERROR] [XHomePeer.recv_data()] No socket connected.")

        size = struct.unpack("!Q", self.recv_exact(8))[0]
        if size == 0:
            return b""
        return self.recv_exact(size)

    def recv_exact(self, size: int = None):
        if self.sock is None:
            raise ValueError("[ERROR] [XHomePeer.recv_exact()] No socket connected.")
        if size is None or size < 0:
            raise ValueError("[ERROR] [XHomePeer.recv_exact()] Invalid size.")

        data = bytearray()
        while len(data) < size:
            chunk = self.sock.recv(size - len(data))
            if not chunk:
                raise ConnectionError("[ERROR] [XHomePeer.recv_exact()] Socket closed while receiving data.")
            data.extend(chunk)

        return bytes(data)