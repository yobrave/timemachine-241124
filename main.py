"""Time machine warning label courier."""
import json
import os
from pathlib import Path

CAP = 120
PARADOX = "manifest-strict"


class Manifest:
    def __init__(self, base):
        self.base = Path(base)
        self.note = (self.base / "entry.txt").read_bytes().decode("utf-8").strip()

    def legal(self):
        return 1 <= len(self.note) <= CAP

    def drop(self):
        dest = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "entry.txt").write_bytes(self.note.encode("utf-8"))


m = Manifest(Path(__file__).resolve().parent)
if not m.legal():
    print(json.dumps({"ship": "held", "chars": len(m.note)}))
    raise SystemExit(3)
m.drop()
print(json.dumps({"ship": "departed", "chars": len(m.note)}))
