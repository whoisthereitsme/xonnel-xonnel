# [!] {+} IMPORTS
from typing import TYPE_CHECKING
# [|] {+} IMPORTS TYPING
if TYPE_CHECKING:
    ...
# [|] {-}


# [|] {+} IMPORTS 3RD PARTY
from pathlib import Path
import json
import os
import queue
import socket
import threading
import time
# [|] {-}
# [!] {-}


class ALog:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 50505,
        proc: str | None = None,
        log: str = "main",
        retry: float = 1.0,
        timeout: float = 2.0,
    ):
        self.host: str = host
        self.port: int = port
        self.proc: str = proc or Path(os.path.abspath(os.sys.argv[0])).stem or "main"
        self.log: str = log
        self.retry: float = retry
        self.timeout: float = timeout

        self.sock: socket.socket | None = None
        self.lock: threading.RLock = threading.RLock()
        self.queue: queue.Queue = queue.Queue()
        self.stop: bool = False
        self.thread: threading.Thread | None = None

        self.init()
        self.post()

    def init(self):
        self.connect()

    def post(self):
        if self.thread and self.thread.is_alive():
            return

        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def connect(self):
        with self.lock:
            self.close()

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                sock.connect((self.host, self.port))
                self.sock = sock
                return True
            except Exception:
                self.sock = None
                return False

    def close(self):
        try:
            if self.sock:
                self.sock.close()
        except Exception:
            pass
        finally:
            self.sock = None

    def build_item(self, text: str = "", typ: str = "log", log: str | None = None):
        return {
            "type": typ,
            "pid": os.getpid(),
            "tid": threading.get_ident(),
            "proc": self.proc,
            "log": log or self.log,
            "time": time.time(),
            "text": str(text),
        }

    def send_item(self, item: dict):
        data = (json.dumps(item, ensure_ascii=False) + "\n").encode("utf-8", errors="replace")

        with self.lock:
            if not self.sock and not self.connect():
                return False

            try:
                self.sock.sendall(data)
                return True
            except Exception:
                self.close()
                return False

    def loop(self):
        while not self.stop:
            try:
                item = self.queue.get(timeout=0.2)
            except queue.Empty:
                continue

            ok = self.send_item(item)
            if ok:
                continue

            while not self.stop:
                if self.connect():
                    if self.send_item(item):
                        break
                time.sleep(self.retry)

    def emit(self, text: str = "", typ: str = "log", log: str | None = None):
        item = self.build_item(text=text, typ=typ, log=log)
        self.queue.put(item)
        return item

    def write(self, text: str = "", log: str | None = None):
        self.emit(text=text, typ="log", log=log)

    def info(self, text: str = "", log: str | None = None):
        self.emit(text=text, typ="info", log=log)

    def warn(self, text: str = "", log: str | None = None):
        self.emit(text=text, typ="warn", log=log)

    def error(self, text: str = "", log: str | None = None):
        self.emit(text=text, typ="error", log=log)

    def debug(self, text: str = "", log: str | None = None):
        self.emit(text=text, typ="debug", log=log)

    def __call__(self, text: str = "", log: str | None = None):
        self.write(text=text, log=log)

    def shutdown(self):
        self.stop = True
        self.close()

    @classmethod
    def load(cls, path: str | Path = None):
        try:
            if path is None:
                print("[ERROR] [ALog.load()] [path=None]")
                return None

            path = Path(path)
            if not path.exists():
                print(f"[ERROR] [ALog.load()] [not found] [{path}]")
                return None

            with open(path, "r", encoding="utf-8") as f:
                return f.read()

        except Exception as e:
            print(f"[ERROR] [ALog.load()] [{e}]")
            return None

    @classmethod
    def save(cls, path: str | Path = None, data: str = None):
        try:
            if path is None:
                print("[ERROR] [ALog.save()] [path=None]")
                return False

            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                f.write("" if data is None else str(data))

            return True

        except Exception as e:
            print(f"[ERROR] [ALog.save()] [{e}]")
            return False

    @classmethod
    def append(cls, path: str | Path = None, data: str = None):
        try:
            if path is None:
                print("[ERROR] [ALog.append()] [path=None]")
                return False

            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "a", encoding="utf-8") as f:
                f.write("" if data is None else str(data))

            return True

        except Exception as e:
            print(f"[ERROR] [ALog.append()] [{e}]")
            return False

    def __repr__(self):
        return f"<ALog proc={self.proc!r} log={self.log!r} host={self.host!r} port={self.port!r}>"










if __name__ == "__main__":
    i = 0
    while True:
        log = ALog()
        log.info("Hello, ALog!")                # -> info and all tabs
        log.warn("This is a warning.")          # -> warn and all tabs
        log.error("This is an error.")          # -> error and all tabs
        log.debug("This is a debug message.")   # -> debug and all tabs
        log.write("This is a log message.")     # -> all tab

        log.write("[ERROR]")                          # to error tab and all tabs
        log.write("[WARN]")                           # to warn tab and all tabs
        log.write("[INFO]")                           # to info tab and all tabs
        log.write("[DEBUG]")                          # to debug tab and all tabs
        log.write("")                                 # to all tab
        time.sleep(1)
        i += 1
        if i >= 1000:
            break
