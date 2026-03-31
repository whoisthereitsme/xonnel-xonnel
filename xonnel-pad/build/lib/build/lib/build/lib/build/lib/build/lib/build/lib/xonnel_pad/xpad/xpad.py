from typing import Any


class XPad:
    NA = "N/A"

    def __init__(self, text: Any = None, fill: str = " ", nlen: int = 10, boolshort: bool = False, na: str = None):
        self.text = text
        self.fill = fill
        self.nlen = nlen
        self.boolshort = boolshort
        self.na = na if na is not None else self.NA
        self.init()

    def init(self):
        self.text = self.normalize(self.text, na=self.na)

        if isinstance(self.text, (list, tuple)):
            if self.isrows(self.text):
                self.text = self.padrows(self.text, fill=self.fill, boolshort=self.boolshort)
            else:
                self.text = self.padall(self.text, fill=self.fill, boolshort=self.boolshort)
        else:
            self.text = self.pad(self.text, fill=self.fill, nlen=self.nlen, boolshort=self.boolshort)

    @classmethod
    def normalize(cls, data, na: str = None):
        na = na if na is not None else cls.NA

        if isinstance(data, dict):
            return cls.dict2rows(data, na=na)

        if isinstance(data, (list, tuple)):
            if not data:
                return []

            if all(isinstance(item, dict) for item in data):
                return cls.listdict2rows(data, na=na)

            out = []
            for item in data:
                if isinstance(item, dict):
                    out.extend(cls.dict2rows(item, na=na))
                else:
                    out.append(item)
            return out

        return data

    @classmethod
    def dict2rows(cls, data: dict = None, na: str = None):
        na = na if na is not None else cls.NA

        if not isinstance(data, dict) or not data:
            return []

        vals = list(data.values())

        if all(isinstance(v, dict) for v in vals):
            headers = []
            for sub in vals:
                for k in sub.keys():
                    if k not in headers:
                        headers.append(k)

            rows = [[""] + headers]
            for rowname, sub in data.items():
                row = [rowname]
                for h in headers:
                    row.append(sub.get(h, na))
                rows.append(row)
            return rows

        if all(isinstance(v, (list, tuple)) for v in vals):
            maxlen = max(len(v) for v in vals) if vals else 0
            headers = [str(i + 1) for i in range(maxlen)]

            rows = [[""] + headers]
            for rowname, sub in data.items():
                row = [rowname] + list(sub)
                while len(row) < maxlen + 1:
                    row.append(na)
                rows.append(row)
            return rows

        return [[k, v] for k, v in data.items()]

    @classmethod
    def listdict2rows(cls, data, na: str = None):
        na = na if na is not None else cls.NA

        if not data:
            return []

        headers = []
        for item in data:
            for k in item.keys():
                if k not in headers:
                    headers.append(k)

        rows = [[""] + headers]
        for i, item in enumerate(data):
            row = [i]
            for h in headers:
                row.append(item.get(h, na))
            rows.append(row)

        return rows

    @classmethod
    def isrows(cls, text):
        if not isinstance(text, (list, tuple)):
            return False
        if not text:
            return False
        return all(isinstance(x, (list, tuple)) for x in text)

    @classmethod
    def isfloatlike(cls, x):
        return isinstance(x, float)

    @classmethod
    def isintlike(cls, x):
        return isinstance(x, int) and not isinstance(x, bool)

    @classmethod
    def totext(cls, x, boolshort: bool = False):
        if isinstance(x, bool):
            if boolshort:
                return "T" if x else "F"
            return str(x)
        if x is None:
            return ""
        return str(x)

    @classmethod
    def pad(cls, text: Any = None, fill: str = " ", nlen: int = 10, boolshort: bool = False):
        s = cls.totext(text, boolshort=boolshort)

        if cls.isintlike(text):
            return s.rjust(nlen, fill)

        return s.ljust(nlen, fill)

    @classmethod
    def padall(cls, texts, fill: str = " ", boolshort: bool = False):
        vals = list(texts)
        if not vals:
            return []

        has_float = any(cls.isfloatlike(v) for v in vals)

        if has_float:
            lefts = []
            rights = []
            raws = []

            for v in vals:
                raw = cls.totext(v, boolshort=boolshort)
                raws.append(raw)

                if cls.isfloatlike(v):
                    s = str(v)
                    if "." in s:
                        l, r = s.split(".", 1)
                    else:
                        l, r = s, ""
                else:
                    l, r = raw, ""

                lefts.append(l)
                rights.append(r)

            max_left = max(len(x) for x in lefts) if lefts else 0
            max_right = max(len(x) for x in rights) if rights else 0
            total = max_left + 1 + max_right if max_right > 0 else max_left

            out = []
            for v, raw in zip(vals, raws):
                if cls.isfloatlike(v):
                    s = str(v)
                    if "." in s:
                        l, r = s.split(".", 1)
                    else:
                        l, r = s, ""
                    out.append(l.rjust(max_left, fill) + "." + r.ljust(max_right, fill))
                else:
                    if cls.isintlike(v):
                        out.append(raw.rjust(total, fill))
                    else:
                        out.append(raw.ljust(total, fill))
            return out

        vals_str = [cls.totext(v, boolshort=boolshort) for v in vals]
        nlen = max(len(v) for v in vals_str)

        out = []
        for v, s in zip(vals, vals_str):
            if cls.isintlike(v):
                out.append(s.rjust(nlen, fill))
            else:
                out.append(s.ljust(nlen, fill))

        return out

    @classmethod
    def padrows(cls, rows, fill: str = " ", boolshort: bool = False):
        rows = [list(row) for row in rows]
        if not rows:
            return []

        ncols = max(len(row) for row in rows)

        for row in rows:
            while len(row) < ncols:
                row.append("")

        cols = list(zip(*rows))
        cols = [cls.padall(col, fill=fill, boolshort=boolshort) for col in cols]

        out = []
        for row in zip(*cols):
            out.append(list(row))

        return out

    @classmethod
    def renderrows(cls, rows, sep: str = " | "):
        return "\n".join(sep.join(str(x) for x in row) for row in rows)

    def __str__(self):
        if isinstance(self.text, list):
            if self.isrows(self.text):
                return self.renderrows(self.text)
            return "\n".join(str(x) for x in self.text)
        return str(self.text)

    def __repr__(self):
        return f"XPad(text={self.text!r}, fill={self.fill!r}, nlen={self.nlen!r}, boolshort={self.boolshort!r}, na={self.na!r})"


















