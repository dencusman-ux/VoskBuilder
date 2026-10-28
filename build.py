#!/usr/bin/env python3
"""Build KageBrowser into a Windows installer.

Pipeline:
    1. PyInstaller -> standalone KageBrowser.exe (onefile, windowed)
    2. Inno Setup -> KageBrowser-<version>-Setup.exe

Usage:
    python build.py --version 0.4.6 [--no-installer] [--clean]
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD_DIR = ROOT / "build"
DIST_DIR = ROOT / "dist"
ARTIFACTS_DIR = ROOT / "artifacts"
ISS_FILE = ROOT / "installer" / "kagebrowser.iss"
SPEC_FILE = ROOT / "KageBrowser.spec"

ISCC_CANDIDATES = [
    Path(os.environ.get("ISCC_PATH", "")),
    Path(r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"),
    Path(r"C:\Program Files\Inno Setup 6\ISCC.exe"),
]


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print(f"$ {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, cwd=cwd or ROOT, check=True)


def clean() -> None:
    for d in (BUILD_DIR, DIST_DIR):
        if d.exists():
            shutil.rmtree(d)


def build_exe(version: str) -> Path:
    os.environ["APP_VERSION"] = version
    run([
        sys.executable, "-m", "PyInstaller",
        str(SPEC_FILE),
        "--noconfirm",
        "--clean",
        "--distpath", str(DIST_DIR),
        "--workpath", str(BUILD_DIR),
    ])
    exe = DIST_DIR / "KageBrowser.exe"
    if not exe.exists():
        raise SystemExit(f"PyInstaller did not produce {exe}")
    return exe


def find_iscc() -> Path | None:
    for cand in ISCC_CANDIDATES:
        if cand and cand.is_file():
            return cand
    found = shutil.which("ISCC")
    return Path(found) if found else None


def build_installer(version: str, exe: Path) -> Path | None:
    iscc = find_iscc()
    if iscc is None:
        print("! Inno Setup (ISCC.exe) not found - skipping installer step.", file=sys.stderr)
        return None
    if not ISS_FILE.exists():
        print(f"! {ISS_FILE} missing - skipping installer step.", file=sys.stderr)
        return None

    ARTIFACTS_DIR.mkdir(exist_ok=True)
    run([str(iscc), f"/DAppVersion={version}", str(ISS_FILE)])

    produced = sorted(ARTIFACTS_DIR.glob("KageBrowser-*-Setup.exe"))
    if not produced:
        produced = sorted(ARTIFACTS_DIR.glob("*Setup.exe"))
    return produced[-1] if produced else None


def main() -> int:
    ap = argparse.ArgumentParser(description="Build KageBrowser installer")
    ap.add_argument("--version", default=os.environ.get("APP_VERSION", "0.0.0"))
    ap.add_argument("--no-installer", action="store_true", help="only build the .exe")
    ap.add_argument("--clean", action="store_true", help="wipe build/ and dist/ first")
    args = ap.parse_args()

    if args.clean:
        clean()

    exe = build_exe(args.version)
    print(f"OK exe: {exe}")

    if not args.no_installer:
        setup = build_installer(args.version, exe)
        if setup:
            print(f"OK installer: {setup}")
        else:
            print("Installer skipped (ISCC missing).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
