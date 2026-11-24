# Time-machine warning label packager for make.fun.
import json
import os
import pathlib
import sys


def load(root):
    text = (pathlib.Path(root) / "entry.txt").read_text(encoding="utf-8")
    return text.strip()


def audit(label):
    problems = []
    if not label:
        problems.append("empty label")
    if len(label.splitlines()) != 1:
        problems.append("not a single line")
    cap = 120  # judge brief allows at most 120 characters
    if len(label) > cap:
        problems.append(f"exceeds {cap} characters")
    return problems


def deliver(root):
    outdir = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    outdir.mkdir(parents=True, exist_ok=True)
    target = outdir / "entry.txt"
    target.write_text(load(root) + "\n", encoding="utf-8")
    return target


if __name__ == "__main__":
    here = pathlib.Path(__file__).resolve().parent
    flaws = audit(load(here))
    if flaws:
        print("gate failed: " + "; ".join(flaws), file=sys.stderr)
        sys.exit(1)
    where = deliver(here)
    print(json.dumps({"copied": str(where), "chars": len(load(here))}))
