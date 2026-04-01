from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...




import json
import queue
import threading





from xonnel_ip import XIp





class XHome:
    LAPTOP = 20000
    DESKTOP = 10000

    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout
        self.localip = XIp.ip()
        self.name = XIp.iam()

        if self.name == "LAPTOP":
            self.hostip   = XIp.LAPTOP
            self.peerip   = XIp.DESKTOP
            self.hostport = XHome.LAPTOP
            self.peerport = XHome.DESKTOP
        elif self.name == "DESKTOP":
            self.hostip   = XIp.DESKTOP
            self.peerip   = XIp.LAPTOP
            self.hostport = XHome.DESKTOP
            self.peerport = XHome.LAPTOP
        else:
            raise RuntimeError(
                "[ERROR] [XHome.__init__()] Could not determine whether this machine is laptop or desktop. "
                f"Detected local ip: {self.localip!r}. Expected {XIp.LAPTOP!r} or {XIp.DESKTOP!r}."
            )

        self.host = XHomeHost(host=self.hostip, port=self.hostport, timeout=self.timeout)
        self.peer = XHomePeer(host=self.peerip, port=self.peerport, timeout=self.timeout)

        self.jobs = queue.Queue()
        self.results = queue.Queue()
        self.running = False
        self.thread = None

        self.start()

    def start(self):
        if self.running:
            return self

        self.running = True
        self.thread = threading.Thread(target=self.loop, daemon=True)
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
            "localip": self.localip,
            "host": {"ip": self.hostip, "port": self.hostport},
            "peer": {"ip": self.peerip, "port": self.peerport},
            "running": self.running,
        }

    def loop(self):
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
                    "error": f"[ERROR] [XHome.loop()] Unknown command: {cmd}",
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
    if home.name == "LAPTOP":
        home.push(src=r"C:\CodeTest\laptop_push.bin", tgt=r"C:\CodeTest\laptop_push.bin")


    if home.name == "DESKTOP":
        home.pull(src=r"C:\CodeTest\desktop_pull.bin", tgt=r"C:\CodeTest\desktop_pull.bin")

    while True:
        time.sleep(1)

else:
    from .xhomehost import XHomeHost
    from .xhomepeer import XHomePeer