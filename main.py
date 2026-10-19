"""
Nexus Performante Arena — launch the performance command center.
Works as .py script or frozen .exe (PyInstaller).
"""
from __future__ import annotations

import os
import sys
import traceback


def _app_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def _bundle_dir() -> str:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return _app_dir()


ROOT = _app_dir()
BUNDLE = _bundle_dir()
if BUNDLE not in sys.path:
    sys.path.insert(0, BUNDLE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# mp3player.py lives next to main in bundle
os.chdir(ROOT)

LOG = os.path.join(ROOT, "launch_error.log")


def _log(msg: str) -> None:
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        pass


def main() -> int:
    try:
        if os.path.isfile(LOG):
            os.remove(LOG)
    except Exception:
        pass

    try:
        from core.hub import run_hub
    except Exception:
        err = traceback.format_exc()
        _log(err)
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                0, err[:1000], "Nexus Performante Arena — import error", 0x10
            )
        except Exception:
            print(err)
        return 1

    try:
        run_hub()
        return 0
    except Exception:
        err = traceback.format_exc()
        _log(err)
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                0, err[:1000], "Nexus Performante Arena — crash", 0x10
            )
        except Exception:
            print(err)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
