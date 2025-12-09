# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-09

### Modernization from Original NRClientX (2010)

This release represents a complete modernization of the original NRClientX GUI client by huhu.tiger (2010), bringing it from Python 2 + wxPython 2.8 to modern standards.

#### Added
- **Python 3.8+ Support** - Complete migration from Python 2.x to Python 3.8+
- **wxPython 4.2.4 (Phoenix)** - Upgraded from wxPython 2.8 to the modern Phoenix rewrite
- **Credential Persistence** - Added `connection.json` for storing last-used login credentials
- **Cross-Platform Path Detection** - Smart auto-detection of `nrclientcmd` across Windows, macOS, and Linux
- **Modern Threading** - Improved subprocess management with proper thread-safe event handling
- **MIT License** - Relicensed modernization work under MIT (original GPL preserved in COPYLEFT.txt)
- **GitHub Repository** - Public repository with proper documentation and version control

#### Changed
- **API Modernization** - Updated all deprecated wxPython 2.x APIs to wxPython 4.x equivalents
- **Event Handling** - Migrated from old-style event binding to modern `wx.PyCommandEvent`
- **Path Handling** - Replaced hardcoded paths with `pathlib.Path` and `shutil.which()`
- **String Handling** - Updated all string operations for Python 3 Unicode compatibility
- **Menu System** - Cleaned up toolbar and menu handling with platform-specific `.def` files

#### Fixed
- **macOS Compatibility** - Fixed path detection for `/Library/NeoRouter/nrclientcmd`
- **Windows Path Detection** - Added fallback paths for various NeoRouter installation locations
- **Subprocess Communication** - Fixed text mode handling for stdin/stdout with Python 3
- **Image Handler Initialization** - Updated to `wx.InitAllImageHandlers()` for wxPython 4.x

#### Technical Improvements
- **Removed Boa Constructor Dependencies** - While preserving Boa-style comments for reference
- **Better Error Handling** - Added FileNotFoundError handling for missing `nrclientcmd`
- **Queue-Based Task Management** - Implemented proper task queue for CLI commands
- **Event-Driven Architecture** - Custom `ResultEvent` for thread-to-UI communication

### Original NRClientX Features (Preserved)
- Buddy list with hierarchical tree view
- Context menu actions (Ping, RDP, SSH) via `menu_*.def` files
- Real-time network status updates
- Computer grouping and categorization
- Cross-platform GUI consistency

---

## Original Author Credit

**Original NRClientX** by huhu.tiger (huhu.tigerx@gmail.com)  
Released under GPL in 2010

**NRClientNext Modernization** by 2ReTz  
Released under MIT License in 2025

---

## Future Roadmap

See [GitHub Issues](https://github.com/2ReTz/NRClientNext/issues) for planned features and enhancements.
