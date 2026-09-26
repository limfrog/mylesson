#!/usr/bin/env python3
"""My Lesson Diary v2.2.5 build.

src/app.js + src/index.template.html -> deploy/index.html
Also copies deploy companion files. Uses local esbuild only when installed; never invokes npx/network.
"""
from pathlib import Path
import json, shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "app.js"
TPL = ROOT / "src" / "index.template.html"
DEPLOY = ROOT / "deploy"
OUT = DEPLOY / "index.html"
MARK = "/*__APP_BUNDLE__*/"


def syntax_check(code: str) -> None:
    node = shutil.which("node")
    if not node:
        print("WARN: node not found; JS syntax check skipped")
        return
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write("try{new Function(" + json.dumps(code) + ");console.log('OK')}catch(e){console.error(e.stack||e.message);process.exit(1)}")
        tmp = f.name
    r = subprocess.run([node, tmp], capture_output=True, text=True)
    Path(tmp).unlink(missing_ok=True)
    if r.returncode:
        sys.exit("JS syntax error:\n" + (r.stderr or r.stdout))
    print("OK: JavaScript syntax")


def maybe_minify(code: str) -> str:
    esbuild = shutil.which("esbuild")
    if not esbuild:
        print("INFO: local esbuild not installed; keeping readable bundle")
        return code
    r = subprocess.run([esbuild, "--minify-whitespace", "--charset=utf8", "--loader=js"],
                       input=code, capture_output=True, text=True)
    if r.returncode:
        sys.exit("esbuild error:\n" + r.stderr)
    return r.stdout.strip()


def static_guard(code: str, tpl: str) -> None:
    if tpl.count(MARK) != 1:
        sys.exit("template must contain exactly one app bundle marker")
    if "</script" in code.lower():
        sys.exit("app.js contains </script and cannot be embedded safely")
    forbidden = ["window.confirm", "window.__gcalCleanup", "window.__requestLockSetup"]
    for token in forbidden:
        if token in code:
            sys.exit(f"stability guard failed: {token} remains")
    if '"2.2.5"' not in code:
        sys.exit("stability guard failed: app version 2.2.5 missing")
    if "serviceWorker.register('./sw.js'" not in tpl:
        sys.exit("stability guard failed: external service worker registration missing")
    if "user-scalable=no" in tpl or "maximum-scale=1" in tpl:
        sys.exit("accessibility guard failed: viewport zoom is disabled")


def main() -> None:
    code = SRC.read_text(encoding="utf-8")
    tpl = TPL.read_text(encoding="utf-8")
    static_guard(code, tpl)
    syntax_check(code)
    bundle = maybe_minify(code)
    DEPLOY.mkdir(exist_ok=True)
    OUT.write_text(tpl.replace(MARK, bundle), encoding="utf-8")
    for name in ["privacy.html", "terms.html", "sw.js", "styles.css", "logo.png", "logo.svg"]:
        src = ROOT / name
        if src.exists():
            shutil.copy2(src, DEPLOY / name)
    print(f"OK: built {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
