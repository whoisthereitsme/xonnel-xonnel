import base64
import zlib
import lzma


class XCodex:
    @classmethod
    def encode(cls, data=None, mode:str="zlib base64"):
        modes = [m for m in mode.split(" ") if m]

        if len(modes) > 1:
            for m in modes:
                data = cls.encode(data=data, mode=m)
            return data

        mode = modes[0]

        if mode == "base64":
            return cls._encode_base64(data=data)

        if mode == "zlib":
            return cls._encode_zlib(data=data)

        if mode == "lzma":
            return cls._encode_lzma(data=data)

        if mode == "hex":
            return cls._encode_hex(data=data)

        if mode == "bin":
            return cls._encode_bin(data=data)

        raise ValueError(f"Unsupported encode mode: {mode}")

    @classmethod
    def decode(cls, data=None, mode:str="zlib base64"):
        modes = [m for m in mode.split(" ") if m]

        if len(modes) > 1:
            for m in reversed(modes):
                data = cls.decode(data=data, mode=m)
            return data

        mode = modes[0]

        if mode == "base64":
            return cls._decode_base64(data=data)

        if mode == "zlib":
            return cls._decode_zlib(data=data)

        if mode == "lzma":
            return cls._decode_lzma(data=data)

        if mode == "hex":
            return cls._decode_hex(data=data)

        if mode == "bin":
            return cls._decode_bin(data=data)

        raise ValueError(f"Unsupported decode mode: {mode}")

    @classmethod
    def _encode_base64(cls, data:bytes=None):
        if data is None:
            return None

        if not isinstance(data, (bytes, bytearray)):
            raise TypeError(f"base64 encode expected bytes, got {type(data).__name__}")

        return base64.b64encode(bytes(data)).decode("utf-8")

    @classmethod
    def _decode_base64(cls, data:str=None):
        if data is None:
            return None

        if not isinstance(data, str):
            raise TypeError(f"base64 decode expected str, got {type(data).__name__}")

        return base64.b64decode(data.encode("utf-8"))

    @classmethod
    def _encode_zlib(cls, data:bytes=None):
        if data is None:
            return None

        if not isinstance(data, (bytes, bytearray)):
            raise TypeError(f"zlib encode expected bytes, got {type(data).__name__}")

        return zlib.compress(bytes(data))

    @classmethod
    def _decode_zlib(cls, data:bytes=None):
        if data is None:
            return None

        if not isinstance(data, (bytes, bytearray)):
            raise TypeError(f"zlib decode expected bytes, got {type(data).__name__}")

        return zlib.decompress(bytes(data))

    @classmethod
    def _encode_lzma(cls, data:bytes=None):
        if data is None:
            return None

        if not isinstance(data, (bytes, bytearray)):
            raise TypeError(f"lzma encode expected bytes, got {type(data).__name__}")

        return lzma.compress(bytes(data))

    @classmethod
    def _decode_lzma(cls, data:bytes=None):
        if data is None:
            return None

        if not isinstance(data, (bytes, bytearray)):
            raise TypeError(f"lzma decode expected bytes, got {type(data).__name__}")

        return lzma.decompress(bytes(data))

    @classmethod
    def _encode_hex(cls, data:int=None):
        if data is None:
            return None

        if not isinstance(data, int):
            raise TypeError(f"hex encode expected int, got {type(data).__name__}")

        return format(data, "x")

    @classmethod
    def _decode_hex(cls, data:str=None):
        if data is None:
            return None

        if not isinstance(data, str):
            raise TypeError(f"hex decode expected str, got {type(data).__name__}")

        return int(data, 16)

    @classmethod
    def _encode_bin(cls, data:int=None):
        if data is None:
            return None

        if not isinstance(data, int):
            raise TypeError(f"bin encode expected int, got {type(data).__name__}")

        return format(data, "b")

    @classmethod
    def _decode_bin(cls, data:str=None):
        if data is None:
            return None

        if not isinstance(data, str):
            raise TypeError(f"bin decode expected str, got {type(data).__name__}")

        return int(data, 2)





















def size(data):
    if data is None:
        return 0

    if isinstance(data, (bytes, bytearray)):
        return len(data)

    if isinstance(data, str):
        return len(data.encode("utf-8"))

    return len(str(data).encode("utf-8"))



def ratio(original, new):
    s1 = size(original)
    s2 = size(new)

    if s1 == 0:
        return 0.0

    return (1 - (s2 / s1)) * 100





def test():
    def show(label, original, encoded, decoded):
        s1 = size(original)
        s2 = size(encoded)
        r = ratio(original, encoded)

        print(f"[{label}]")
        print(f"original size : {s1} bytes")
        print(f"encoded size  : {s2} bytes")
        print(f"ratio         : {r:.2f}%")
        print(f"valid         : {original == decoded}")
        print()

    # base64
    a = b"hello world"
    b = XCodex.encode(a, mode="base64")
    c = XCodex.decode(b, mode="base64")

    show("base64", a, b, c)

    # hex
    x = 255
    y = XCodex.encode(x, mode="hex")
    z = XCodex.decode(y, mode="hex")

    print("[hex int]")
    print(x, y, z, x == z)
    print()

    # bin
    p = 255
    q = XCodex.encode(p, mode="bin")
    r = XCodex.decode(q, mode="bin")

    print("[bin int]")
    print(p, q, r, p == r)
    print()

    # zlib + base64
    d1 = b"hello world" * 10000
    d2 = XCodex.encode(d1, mode="zlib base64")
    d3 = XCodex.decode(d2, mode="zlib base64")

    show("zlib base64", d1, d2, d3)

    # lzma + base64
    e1 = b"hello world" * 10000
    e2 = XCodex.encode(e1, mode="lzma base64")
    e3 = XCodex.decode(e2, mode="lzma base64")

    show("lzma base64", e1, e2, e3)


if __name__ == "__main__":
    test()