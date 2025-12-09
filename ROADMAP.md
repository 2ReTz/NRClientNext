# 🗺️ NRClientNext Roadmap

This document tracks the detailed feature roadmap and backlog for **NRClientNext**. It outlines our vision for modernizing the client, improving security, and adding new capabilities.

> [!NOTE]
> This is a living document. Priorities may change based on user feedback and technical requirements.

## 🚀 Upcoming Release (v1.0.0 Target)

### 🔒 Security & Persistence
- [ ] **Secure Credential Storage**: Migrate from plain-text `connection.json` to system native secure storage (using `keyring` library).
  - *Context*: Currently, passwords are stored in `connection.json`. This is legacy behavior that needs immediate modernization.

### 🛠️ Stability & DevOps
- [ ] **Logging System**: Implement Python's standard `logging` module to replace print statements and provide rotating log files for debugging.
- [ ] **CI/CD Pipeline**: Setup GitHub Actions for:
  - Automated Linting (`flake8`/`pylint`)
  - Type Checking (`mypy`)
  - Build Verification (ensure it packages correctly)

## 🔮 Future Enhancements (Backlog)

### 🎨 UI/UX Polish
- [ ] **Dark Mode Support**: Detect system theme and switch to a dark color palette.
- [ ] **System Tray Icon**: Minimize to tray instead of closing, with a context menu for quick connect/disconnect.
- [ ] **Configurable Refresh**: Add settings dialog to control how often the buddy list updates.
- [ ] **High DPI Icons**: Replace older bitmap icons with SVG or high-res PNGs for 4K displays.

### ⚡ Feature Expansion
- [ ] **Export Buddy List**: Capability to export the current list to CSV/JSON.
- [ ] **Multi-Profile Support**: Better handling for switching between different NeoRouter domains/users without re-typing credentials.
- [ ] **Quick Connect History**: Dropdown in the login dialog showing recently used domains.

### 🏗️ Technical Debt & Architecture
- [ ] **Unit Testing**: Add `pytest` suite for core logic (parsing CLI output, state management).
- [ ] **Validation Layer**: Add strict validation for input fields in `Logon.py`.
- [ ] **Menu Refactoring**: Move away from `.def` files to a proper Python-based menu definition structure to reduce I/O on startup.

## ✅ Completed Milestones
- **Modernization**: Ported from Python 2/wxPython 2.8 to Python 3/wxPython 4 (Phoenix).
- **Cross-Platform**: Unified codebase for Windows, macOS, and Linux.
- **UI Modernization**: Replaced absolute positioning with responsive Sizers.
- **Stability**: Fixed critical crash in Context Menus (ID ref-counting).
