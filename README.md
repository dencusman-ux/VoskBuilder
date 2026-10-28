# KageBuilder

Build pipeline for **KageBrowser** — packages the Python/PyQt6 source into a
standalone Windows installer.

```
source ──▶ PyInstaller ──▶ KageBrowser.exe ──▶ Inno Setup ──▶ KageBrowser-<ver>-Setup.exe
```

## What is inside

| Path | Purpose |
|------|---------|
| `KageBrowser.spec` | PyInstaller build spec (onefile, no console) |
| `build.py` | Orchestrates PyInstaller + Inno Setup |
| `installer/kagebrowser.iss` | Inno Setup script (RU/EN languages) |
| `requirements.txt` | Build dependencies |
| `.github/workflows/build.yml` | CI: builds on push/tag, uploads artifact + release |

## Local build

```bash
pip install -r requirements.txt
python build.py --version 0.4.6 --clean
```

Needs [Inno Setup 6](https://jrsoftware.org/isdl.php) for the installer step
(skip with `--no-installer` to only get the `.exe`).

The app source itself lives in the
[KageBrowser](https://github.com/dencusman-ux/KageBrowser) repository —
point `KageBrowser.spec` at your `main.py` entry point.

## CI

Push to `main` or tag `vX.Y.Z`. Tagged pushes create a GitHub release with the
installer attached; every run uploads `KageBrowser-installer` as an artifact.
