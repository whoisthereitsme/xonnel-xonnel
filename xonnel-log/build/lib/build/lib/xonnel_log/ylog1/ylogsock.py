from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ylog import YLog

import json
import queue
import socket
import threading
import time


class LogSock:
    def __init__(self, ylog: "YLog"):
        self.ylog: YLog = ylog

        self.init()
        self.post()

    def init(self):
        self.host: str = self.ylog.cfg.host
        self.port: int = self.ylog.cfg.port

        self.server: socket.socket | None = None
        self.thread: threading.Thread | None = None
        self.stop: bool = False

        self.lock: threading.RLock = threading.RLock()
        self.events: queue.Queue = queue.Queue()

        self.data: dict = {}
        self.clients: list[threading.Thread] = []

    def post(self):
        if self.thread and self.thread.is_alive():
            return

        self.stop = False
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def loop(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen()
            self.server.settimeout(0.5)
        except Exception as e:
            print(f"[ERROR] [LogSock.loop] server init failed: {e}")
            return

        while not self.stop:
            try:
                conn, addr = self.server.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            except Exception:
                continue

            worker = threading.Thread(
                target=self.handle_client,
                args=(conn, addr),
                daemon=True,
            )
            worker.start()

            with self.lock:
                self.clients.append(worker)

        try:
            if self.server:
                self.server.close()
        except Exception:
            pass

    def handle_client(self, conn: socket.socket, addr):
        buffer = b""

        try:
            while not self.stop:
                chunk = conn.recv(4096)
                if not chunk:
                    break

                buffer += chunk

                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    line = line.strip()

                    if not line:
                        continue

                    try:
                        item = json.loads(line.decode("utf-8", errors="replace"))
                        if isinstance(item, dict):
                            self.handle_item(item=item, addr=addr)
                    except Exception:
                        pass

        except Exception:
            pass

        finally:
            try:
                conn.close()
            except Exception:
                pass

    def handle_item(self, item: dict, addr=None):
        pid: int = item.get("pid")
        tid: int = item.get("tid")
        proc: str = item.get("proc") or "main"
        log: str = item.get("log") or "main"
        typ: str = item.get("type") or "log"
        ts: float = item.get("time", time.time())
        text: str = item.get("text", "")

        with self.lock:
            if proc not in self.data:
                self.data[proc] = {}

            if log not in self.data[proc]:
                self.data[proc][log] = {
                    "msgs": [],
                    "proc": proc,
                    "log": log,
                    "created": ts,
                }

            if typ == "log":
                msg = {
                    "time": ts,
                    "text": text,
                    "pid": pid,
                    "tid": tid,
                    "proc": proc,
                    "log": log,
                }
                self.data[proc][log]["msgs"].append(msg)

            self.events.put({
                "type": typ,
                "pid": pid,
                "tid": tid,
                "proc": proc,
                "log": log,
                "time": ts,
                "text": text,
            })

    def get_event_nowait(self):
        try:
            return self.events.get_nowait()
        except queue.Empty:
            return None

    def get_data(self):
        with self.lock:
            out = {}
            for proc, logs in self.data.items():
                out[proc] = {}
                for log, info in logs.items():
                    out[proc][log] = {
                        "msgs": list(info["msgs"]),
                        "proc": info["proc"],
                        "log": info["log"],
                        "created": info["created"],
                    }
            return out

    def shutdown(self):
        self.stop = True

        try:
            if self.server:
                self.server.close()
        except Exception:
            pass