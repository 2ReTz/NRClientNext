# NRClientNext
Python 3 + wxPython 4 refresh of the NeoRouter NRClientX GUI. Includes modernized APIs, Windows/macOS/Linux support   for nrclientcmd, credential persistence, and updated toolbar/menu handling.
Python 3 + wxPython 4 refresh of the NeoRouter NRClientX GUI. Modernized APIs, better Windows/macOS/Linux
  compatibility for `nrclientcmd`, credential persistence, and cleaned-up toolbar/menu handling.

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

  ## Notes

  - connection.json stores the last-used credentials locally in plaintext (ignored by git).
  - If nrclientcmd lives elsewhere, add it to PATH or update the search paths in CLIWrapper.py.
