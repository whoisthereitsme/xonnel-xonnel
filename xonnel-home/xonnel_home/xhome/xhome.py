from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import json
import queue
import socket
import threading


class XHome:
    LAPTOP = "192.168.0.25"
    DESKTOP = "192.168.0.104"

    PORT_LAPTOP = 20000
    PORT_DESKTOP = 10000

    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout
        self.local_ip = self._detect_local_ip()

        if self.local_ip == self.LAPTOP:
            self.name = "laptop"
            self.host_ip = self.LAPTOP
            self.peer_ip = self.DESKTOP
            self.host_port = self.PORT_LAPTOP
            self.peer_port = self.PORT_DESKTOP
        elif self.local_ip == self.DESKTOP:
            self.name = "desktop"
            self.host_ip = self.DESKTOP
            self.peer_ip = self.LAPTOP
            self.host_port = self.PORT_DESKTOP
            self.peer_port = self.PORT_LAPTOP
        else:
            raise RuntimeError(
                "[ERROR] [XHome.__init__()] Could not determine whether this machine is laptop or desktop. "
                f"Detected local ip: {self.local_ip!r}. Expected {self.LAPTOP!r} or {self.DESKTOP!r}."
            )

        self.host = XHomeHost(host=self.host_ip, port=self.host_port, timeout=self.timeout)
        self.peer = XHomePeer(host=self.peer_ip, port=self.peer_port, timeout=self.timeout)

        self.jobs = queue.Queue()
        self.results = queue.Queue()
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
        self.jobs.put(None)

        try:
            self.host.stop()
        except Exception:
            ...

        return self

    def push(self, src=None, tgt=None):
        self.jobs.put({
            "cmd": "push",
            "src": src,
            "tgt": tgt,
        })
        return self

    def pull(self, src=None, tgt=None):
        self.jobs.put({
            "cmd": "pull",
            "src": src,
            "tgt": tgt,
        })
        return self

    def result(self, block: bool = False, timeout: float = None):
        try:
            if block:
                return self.results.get(timeout=timeout)
            return self.results.get_nowait()
        except queue.Empty:
            return None

    def info(self):
        return {
            "name": self.name,
            "local_ip": self.local_ip,
            "host": {"ip": self.host_ip, "port": self.host_port},
            "peer": {"ip": self.peer_ip, "port": self.peer_port},
            "running": self.running,
        }

    def _loop(self):
        while self.running:
            job = self.jobs.get()

            if job is None:
                break

            try:
                cmd = job["cmd"]

                if cmd == "push":
                    out = self.peer.push(src=job["src"], tgt=job["tgt"])
                    self.results.put(out)
                    continue

                if cmd == "pull":
                    out = self.peer.pull(src=job["src"], tgt=job["tgt"])
                    self.results.put(out)
                    continue

                self.results.put({
                    "ok": False,
                    "error": f"[ERROR] [XHome._loop()] Unknown command: {cmd}",
                    "job": job,
                })

            except Exception as e:
                self.results.put({
                    "ok": False,
                    "error": str(e),
                    "job": job,
                })

    


if __name__ == "__main__":
    import time
    from xhomehost import XHomeHost
    from xhomepeer import XHomePeer

    home = XHome(timeout=3600.0)

    print(json.dumps(home.info(), indent=4))

    if home.name == "laptop":
        home.push(src="laptop_local.bin", tgt="desktop_from_laptop.bin")
    else:
        home.pull(src="desktop_from_laptop.bin", tgt="desktop_copy.bin")

    while True:
        result = home.result()
        if result is not None:
            print(json.dumps(result, indent=4))
        time.sleep(0.1)

else:
    from .xhomehost import XHomeHost
    from .xhomepeer import XHomePeer