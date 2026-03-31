from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ylog import YLog

import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk


class LogApp:
    def __init__(self, ylog: "YLog"):
        self.ylog: YLog = ylog
        self.logsocket = self.ylog.sock
        self.iconpath = Path(self.ylog.cfg.icon) if self.ylog.cfg.icon else None

        self.root = tk.Tk()
        self.root.title(self.ylog.cfg.name)
        self.root.geometry(self.ylog.cfg.geom)

        if self.iconpath and self.iconpath.exists():
            try:
                self.root.iconbitmap(str(self.iconpath))
            except Exception:
                pass

        self.process_tabs = ttk.Notebook(self.root)
        self.process_tabs.pack(fill="both", expand=True)

        self.process_pages: dict = {}
        self.log_pages: dict = {}

        self.hidden: bool = False
        self.root.protocol("WM_DELETE_WINDOW", self.hide)

        self.root.after(self.poll_ms, self.poll)

    @property
    def poll_ms(self) -> int:
        try:
            return max(1, int(float(self.ylog.cfg.poll) * 1000))
        except Exception:
            return 100

    def fmt_time(self, ts):
        dt = datetime.datetime.fromtimestamp(ts)
        return dt.strftime("%H:%M:%S")

    def ensure_process_tab(self, proc: str):
        if proc in self.process_pages:
            return self.process_pages[proc]

        frame = ttk.Frame(self.process_tabs)
        notebook = ttk.Notebook(frame)
        notebook.pack(fill="both", expand=True)

        self.process_tabs.add(frame, text=proc)

        self.process_pages[proc] = {
            "frame": frame,
            "notebook": notebook,
        }
        self.log_pages[proc] = {}

        return self.process_pages[proc]

    def ensure_log_tab(self, proc: str, log: str):
        self.ensure_process_tab(proc)

        if log in self.log_pages[proc]:
            return self.log_pages[proc][log]

        notebook = self.process_pages[proc]["notebook"]
        frame = ttk.Frame(notebook)

        text = tk.Text(frame, wrap="none")
        yscroll = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        xscroll = ttk.Scrollbar(frame, orient="horizontal", command=text.xview)

        text.configure(
            yscrollcommand=yscroll.set,
            xscrollcommand=xscroll.set,
        )

        text.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        notebook.add(frame, text=log)

        self.log_pages[proc][log] = {
            "frame": frame,
            "text": text,
        }

        return self.log_pages[proc][log]

    def append_message(self, proc, log, ts, text, pid=None, tid=None):
        page = self.ensure_log_tab(proc, log)
        box = page["text"]

        prefix = f"[{self.fmt_time(ts)}]"
        if pid is not None and tid is not None:
            prefix += f" [{pid}:{tid}]"

        line = f"{prefix} {text}\n"
        box.insert("end", line)
        box.see("end")

    def poll(self):
        while True:
            event = self.logsocket.get_event_nowait()
            if event is None:
                break

            proc = event["proc"]
            log = event["log"]

            self.ensure_process_tab(proc)
            self.ensure_log_tab(proc, log)

            if event["type"] == "log":
                self.append_message(
                    proc=proc,
                    log=log,
                    ts=event["time"],
                    text=event["text"],
                    pid=event.get("pid"),
                    tid=event.get("tid"),
                )

        self.root.after(self.poll_ms, self.poll)

    def show(self):
        self.hidden = False
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def hide(self):
        self.hidden = True
        self.root.withdraw()

    def quit(self):
        try:
            self.root.withdraw()
        except Exception:
            pass

        try:
            self.root.quit()
        except Exception:
            pass

        try:
            self.root.destroy()
        except Exception:
            pass

    def run(self):
        self.root.mainloop()