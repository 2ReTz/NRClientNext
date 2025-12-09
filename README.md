# NRClientNext

**A modern Python 3 + wxPython 4 refresh of the NeoRouter NRClientX GUI client.**

## 🚀 What's New in NRClientNext

This is a complete modernization of the original [NRClientX](https://github.com/huhu-tiger/NRClientX) (2010) by huhu.tiger, bringing it from **Python 2 + wxPython 2.8** to modern standards:

- ✅ **Python 3.8+ Compatible** - Migrated from legacy Python 2.x
- ✅ **wxPython 4.2.4 (Phoenix)** - Upgraded from wxPython 2.8 classic
- ✅ **Cross-Platform** - Enhanced Windows/macOS/Linux support with smart path detection
- ✅ **Credential Persistence** - Auto-save/load login credentials via `connection.json`
- ✅ **Modern APIs** - All deprecated wxPython calls updated to current standards
- ✅ **Better Threading** - Improved subprocess management and event handling

See [CHANGELOG.md](CHANGELOG.md) for complete upgrade details.

  ## Features
  - Python 3.8+ / wxPython 4 (Phoenix) compatible UI
  - Auto-detects `nrclientcmd` (Windows: PATH, `C:\Program Files\NeoRouter\`, `C:\Program Files (x86)\NeoRouter\`, `C:
  \Program Files (x86)\ZebraNetworkSystems\NeoRouter\NRClientCmd.exe`; macOS: `/Library/NeoRouter/nrclientcmd`)
  - Credential persistence to `connection.json` (plaintext; delete if undesired)
  - Context menu actions via `menu_*.def` (Ping, RDP, SSH, etc.)

  ## Requirements
  - Python 3.8+
  - wxPython 4.2.4 (`pip install -r requirements.txt`)
  - NeoRouter command-line client (`nrclientcmd`) installed and reachable

  ## Setup
  ```bash
  # Optional: create and activate a virtualenv
  pip install -r requirements.txt
  python PyNRClientX.py

  ## Usage

  1. Launch python PyNRClientX.py
  2. Sign in with your domain/username/password
  3. Buddy list populates; right-click a machine for actions from menu_*.def

  ## Credits

  **Original NRClientX** by [huhu.tiger](mailto:huhu.tigerx@gmail.com) (2010)  
  Licensed under GPL - see [COPYLEFT.txt](COPYLEFT.txt)

  **NRClientNext Modernization** by [2ReTz](https://github.com/2ReTz) (2025)  
  Licensed under MIT - see [LICENSE](LICENSE)

  ## Notes

  - connection.json stores the last-used credentials locally in plaintext (ignored by git).
  - If nrclientcmd lives elsewhere, add it to PATH or update the search paths in CLIWrapper.py.
