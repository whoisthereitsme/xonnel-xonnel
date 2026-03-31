import sys
import inspect
import importlib
import importlib.metadata
from pathlib import Path

SKIP_MODULES = {
    "this",
    "antigravity",
    "__hello__",
    "__phello__",
    "idlelib",
    "tkinter",
    "turtle",
}
OUTPATH = Path(r"C:\Code\Python\Packages\xonnel-sys\xonnel_sys\xsys\xsys.py")


# =========================================================
# HELPERS
# =========================================================
def safe_text(value):
    if value is None:
        return "N/A"
    return str(value)


def class_name_from_module(module_name: str) -> str:
    parts = [p for p in module_name.replace("-", "_").split(".") if p]
    name = "_".join(p[:1].upper() + p[1:] for p in parts)
    return f"X{name}"


def normalize_import_name(name: str) -> str:
    return name.strip().replace("-", "_")


def get_stdlib_names() -> list[str]:
    names = set()

    if hasattr(sys, "stdlib_module_names"):
        for name in sys.stdlib_module_names:
            if name and not name.startswith("_"):
                names.add(name)

    return sorted(names)


def get_pip_top_level_names() -> list[str]:
    names = set()

    for dist in importlib.metadata.distributions():
        try:
            txt = dist.read_text("top_level.txt")
        except Exception:
            txt = None

        if txt:
            for line in txt.splitlines():
                line = normalize_import_name(line)
                if line and not line.startswith("_"):
                    names.add(line)
        else:
            try:
                name = dist.metadata.get("Name")
            except Exception:
                name = None

            if name:
                name = normalize_import_name(name)
                if name and not name.startswith("_"):
                    names.add(name)

    return sorted(names)


def try_import_module(name: str):
    try:
        return importlib.import_module(name)
    except Exception:
        return None


def collect_modules() -> tuple[list[object], list[str], list[str]]:
    imported = {}
    failed = []

    candidate_names = []
    candidate_names.extend(get_stdlib_names())
    candidate_names.extend(get_pip_top_level_names())

    # dedupe while preserving sorted-ish order
    seen = set()
    unique_names = []
    for name in candidate_names:
        if name not in seen:
            seen.add(name)
            unique_names.append(name)

    for name in unique_names:
        if name in SKIP_MODULES:
            continue

        mod = try_import_module(name)
        if mod is not None:
            imported[name] = mod
        else:
            failed.append(name)

    modules = [imported[name] for name in sorted(imported)]
    names = sorted(imported)
    failed = sorted(set(failed))

    return modules, names, failed


def build_import_block(module_names: list[str]) -> str:
    lines = []
    for name in module_names:
        lines.append(f"import {name}")
    return "\n".join(lines)


def write_doc(module, attr_name):
    obj = getattr(module, attr_name)
    doc = inspect.getdoc(obj)

    txt = f"        # {module.__name__}.{attr_name}\n"
    txt += f"        self.{attr_name} = {module.__name__}.{attr_name}\n"

    if doc:
        for line in doc.splitlines():
            txt += f"        # {safe_text(line).rstrip()}\n"
    else:
        txt += f"        # N/A\n"

    txt += "\n"
    return txt


def build_module_class(module):
    module_name = module.__name__
    cls_name = class_name_from_module(module_name)

    txt = f"class {cls_name}:\n"
    txt += "    def __init__(self):\n\n"

    for attr_name in dir(module):
        if attr_name.startswith("_"):
            continue

        try:
            txt += write_doc(module, attr_name)
        except Exception as e:
            txt += f"        # {module_name}.{attr_name}\n"
            txt += f"        self.{attr_name} = {module_name}.{attr_name}\n"
            txt += f"        # ERROR: {type(e).__name__}: {e}\n\n"

    txt += "\n"
    return txt


# =========================================================
# MAIN
# =========================================================
def main():
    modules, module_names, failed_names = collect_modules()

    txt = ""
    txt += "# AUTO-GENERATED FILE\n"
    txt += "# Generated from stdlib + installed importable packages\n\n"

    txt += build_import_block(module_names)
    txt += "\n\n\n"

    txt += "FAILED_IMPORTS = [\n"
    for name in failed_names:
        txt += f"    {name!r},\n"
    txt += "]\n\n\n"

    txt += "IMPORTED_MODULES = [\n"
    for name in module_names:
        txt += f"    {name},\n"
    txt += "]\n\n\n"

    for module in modules:
        try:
            txt += build_module_class(module)
            txt += "\n" * 4
        except Exception as e:
            txt += f"# ERROR BUILDING MODULE {module.__name__}: {type(e).__name__}: {e}\n\n"

    OUTPATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPATH, "w", encoding="utf-8") as f:
        f.write(txt)

    print(f"[OK] wrote: {OUTPATH}")
    print(f"[IMPORTED] {len(module_names)} modules")
    print(f"[FAILED]   {len(failed_names)} modules")


if __name__ == "__main__":
    main()