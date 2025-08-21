import argparse, os, pathlib, subprocess, sys
from rich import print
from .llm import make_llm
from .generator import generate_tests_for_source
from .repair import repair_test

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
TESTS_DIR = ROOT / "tests"

def cmd_generate(file: str = None, dir: str = None):
    llm = make_llm()
    created = []
    if file:
        p = pathlib.Path(file)
        name = p.stem
        src = p.read_text(encoding="utf-8")
        code = generate_tests_for_source(src, name, llm)
        outp = TESTS_DIR / f"test_{name}.py"
        outp.write_text(code, encoding="utf-8")
        created.append(str(outp))
    elif dir:
        d = pathlib.Path(dir)
        for p in sorted(d.glob("*.py")):
            name = p.stem
            src = p.read_text(encoding="utf-8")
            code = generate_tests_for_source(src, name, llm)
            outp = TESTS_DIR / f"test_{name}.py"
            outp.write_text(code, encoding="utf-8")
            created.append(str(outp))
    print("[bold]Gerados:[/bold]")
    for c in created:
        print("-", c)

def run_pytest() -> str:
    res = subprocess.run([sys.executable, "-m", "pytest", "-q", "tests", "--disable-warnings", "-q"], capture_output=True, text=True)
    out = (res.stdout or "") + "\n" + (res.stderr or "")
    print(out)
    return out

def cmd_test():
    run_pytest()

def cmd_repair(module: str):
    llm = make_llm()
    test_file = TESTS_DIR / f"test_{module}.py"
    if not test_file.exists():
        print(f"Teste não encontrado: {test_file}")
        sys.exit(1)
    log = run_pytest()
    if "FAILED" in log or "ERROR" in log:
        cur = test_file.read_text(encoding="utf-8")
        fixed = repair_test(module, cur, log, llm)
        test_file.write_text(fixed, encoding="utf-8")
        print("[bold]Re-testando[/bold]")
        run_pytest()

def main():
    ap = argparse.ArgumentParser(prog="testgen")
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate")
    g.add_argument("--file")
    g.add_argument("--dir")

    t = sub.add_parser("test")

    r = sub.add_parser("repair")
    r.add_argument("--module", required=True)

    args = ap.parse_args()
    if args.cmd == "generate":
        cmd_generate(args.file, args.dir)
    elif args.cmd == "test":
        cmd_test()
    elif args.cmd == "repair":
        cmd_repair(args.module)

if __name__ == "__main__":
    main()
