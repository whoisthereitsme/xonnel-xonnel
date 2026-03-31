from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ylog import YLog

import colorsys
import json
import queue
import re
import socket
import threading
import time

from xonnel_emoji import XEmoji


class LogSock:
    EMOJIS = XEmoji().MAPPING
    RE_TAG = re.compile(r"\[([^\[\]]+)\]")

    ANSI_RESET = "\033[0m"

    TYPE_COLORS = {
        "error": "#ff4d4f",
        "warn":  "#faad14",
        "info":  "#40a9ff",
        "debug": "#b37feb",
    }

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

    def normalize_tag(self, txt: str = None):
        if txt is None:
            return None

        txt = str(txt).strip().upper()
        txt = txt.replace("-", "_").replace(" ", "_")
        txt = re.sub(r"[^A-Z0-9_]+", "_", txt)
        txt = re.sub(r"_+", "_", txt)
        txt = txt.strip("_")
        return txt or None

    def key_to_color(self, key: str = None, typ: str = None):
        if typ in self.TYPE_COLORS:
            return self.TYPE_COLORS[typ]

        key = self.normalize_tag(key)
        if not key:
            return "#d9d9d9"

        h = hash(key) & 0xFFFFFFFF
        hue = (h % 360) / 360.0
        sat = 0.70 + (((h >> 8) % 20) / 100.0)
        val = 0.88 + (((h >> 16) % 10) / 100.0)

        r, g, b = colorsys.hsv_to_rgb(hue, min(sat, 1.0), min(val, 1.0))
        return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

    def hex_to_rgb(self, color: str):
        color = str(color).strip().lstrip("#")
        if len(color) != 6:
            return 255, 255, 255
        return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)

    def color_ansi(self, txt: str, color: str):
        r, g, b = self.hex_to_rgb(color)
        return f"\033[38;2;{r};{g};{b}m{txt}{self.ANSI_RESET}"

    def parse_text_parts(self, txt: str = None, typ: str = None):
        txt = "" if txt is None else str(txt)
        out = []
        pos = 0

        for match in self.RE_TAG.finditer(txt):
            a, b = match.span()

            if a > pos:
                raw = txt[pos:a]
                out.append({
                    "kind": "text",
                    "raw": raw,
                    "text": raw,
                    "color": None,
                    "ansi": raw,
                    "key": None,
                    "emoji": None,
                })

            raw_tag = match.group(0)
            raw_key = match.group(1)
            key = self.normalize_tag(raw_key)
            emoji = self.EMOJIS.get(key) if key else None

            if emoji:
                color = self.key_to_color(key=key, typ=typ)
                out.append({
                    "kind": "emoji",
                    "raw": raw_tag,
                    "text": emoji,
                    "color": color,
                    "ansi": self.color_ansi(emoji, color),
                    "key": key,
                    "emoji": emoji,
                })
            else:
                out.append({
                    "kind": "text",
                    "raw": raw_tag,
                    "text": raw_tag,
                    "color": None,
                    "ansi": raw_tag,
                    "key": None,
                    "emoji": None,
                })

            pos = b

        if pos < len(txt):
            raw = txt[pos:]
            out.append({
                "kind": "text",
                "raw": raw,
                "text": raw,
                "color": None,
                "ansi": raw,
                "key": None,
                "emoji": None,
            })

        return out

    def replace_emoji_tags(self, txt: str = None, typ: str = None):
        parts = self.parse_text_parts(txt=txt, typ=typ)
        text = "".join(part["text"] for part in parts)
        text_ansi = "".join(part["ansi"] for part in parts)
        return text, text_ansi, parts

    def handle_item(self, item: dict, addr=None):
        pid: int = item.get("pid")
        tid: int = item.get("tid")
        proc: str = item.get("proc") or "main"
        base_log: str = item.get("log") or "main"
        typ: str = str(item.get("type") or "log").lower()
        ts: float = item.get("time", time.time())
        raw_text: str = str(item.get("text", ""))

        text, text_ansi, parts = self.replace_emoji_tags(txt=raw_text, typ=typ)
        sublog: str = self.route_log(log=base_log, typ=typ, text=raw_text)

        msg = {
            "type": typ,
            "time": ts,
            "text": text,
            "text_ansi": text_ansi,
            "parts": parts,
            "raw_text": raw_text,
            "pid": pid,
            "tid": tid,
            "proc": proc,
            "log": sublog,
            "base_log": base_log,
        }

        with self.lock:
            self.ensure_store(proc=proc, log=sublog, ts=ts)
            self.data[proc][sublog]["msgs"].append(msg)

            self.events.put({
                "type": typ,
                "pid": pid,
                "tid": tid,
                "proc": proc,
                "log": sublog,
                "base_log": base_log,
                "time": ts,
                "text": text,
                "text_ansi": text_ansi,
                "parts": parts,
                "raw_text": raw_text,
            })

            if sublog != "all":
                msg_all = {
                    "type": typ,
                    "time": ts,
                    "text": text,
                    "text_ansi": text_ansi,
                    "parts": parts,
                    "raw_text": raw_text,
                    "pid": pid,
                    "tid": tid,
                    "proc": proc,
                    "log": "all",
                    "base_log": base_log,
                }

                self.ensure_store(proc=proc, log="all", ts=ts)
                self.data[proc]["all"]["msgs"].append(msg_all)

                self.events.put({
                    "type": typ,
                    "pid": pid,
                    "tid": tid,
                    "proc": proc,
                    "log": "all",
                    "base_log": base_log,
                    "time": ts,
                    "text": text,
                    "text_ansi": text_ansi,
                    "parts": parts,
                    "raw_text": raw_text,
                })

    def ensure_store(self, proc: str, log: str, ts: float):
        if proc not in self.data:
            self.data[proc] = {}

        if log not in self.data[proc]:
            self.data[proc][log] = {
                "msgs": [],
                "proc": proc,
                "log": log,
                "created": ts,
            }

    def route_log(self, log: str, typ: str, text: str) -> str:
        up = str(text).upper().strip()

        if "[ERROR]" in up or typ == "error":
            return "error"

        if "[WARN]" in up or typ == "warn":
            return "warn"

        if "[INFO]" in up or typ == "info":
            return "info"

        if "[DEBUG]" in up or typ == "debug":
            return "debug"

        if typ == "log":
            return "all"

        return log or "all"

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