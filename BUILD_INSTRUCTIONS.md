# Building Windows Executable

This guide explains how to package the Screensaver application as a Windows executable (.exe).

## Prerequisites

- Python 3.7 or higher installed on Windows
- All project dependencies installed

## Method 1: Using PyInstaller (Recommended)

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Build the Executable

Run one of the following commands from the project root directory:

**Option A: Using the spec file (recommended)**
```bash
python3 -m PyInstaller build_windows.spec
```

**Option B: One-line command**
```bash
python3 -m PyInstaller --onefile --windowed --name ScreensaverApp --hidden-import screensaver_base --hidden-import color_wheel_screensaver --hidden-import inspirational_quotes_screensaver --add-data "quotes.txt:." main.py
```

**Note:** If `pyinstaller` is in your PATH, you can use `pyinstaller` directly instead of `python3 -m PyInstaller`.

### Step 3: Find Your Executable

After the build completes, you'll find:
- The executable at: `dist/ScreensaverApp.exe`
- Build files in the `build/` folder (can be deleted)

### Step 4: Test the Executable

Simply double-click `ScreensaverApp.exe` or run it from the command line:
```bash
cd dist
ScreensaverApp.exe
```

## Build Options Explained

- `--onefile`: Creates a single executable file (instead of a folder with dependencies)
- `--windowed`: Hides the console window (for GUI apps)
- `--name`: Sets the name of the executable
- `--hidden-import`: Explicitly includes modules that PyInstaller might miss
- `--icon=path/to/icon.ico`: (Optional) Adds a custom icon to your .exe

## Adding a Custom Icon

1. Create or download a `.ico` file (or convert the existing `icons8-painting-64.png`)
2. Place it in the project root (e.g., `screensaver.ico`)
3. Update the spec file or add to command:
   ```bash
   python3 -m PyInstaller --icon=screensaver.ico build_windows.spec
   ```

## Troubleshooting

### "Module not found" errors
If you get import errors, add the missing module to `hiddenimports` in the spec file or use `--hidden-import module_name`.

### Executable is too large
- Use UPX compression (already enabled in spec file)
- Consider using `--exclude-module` to remove unused libraries

### Antivirus false positives
PyInstaller executables sometimes trigger antivirus warnings. This is normal. You can:
- Add an exception to your antivirus
- Sign the executable with a code signing certificate
- Use `--clean` flag and rebuild

### Console appears briefly
Set `console=False` in the spec file (already configured).

## Clean Build

To do a completely fresh build:
```bash
python3 -m PyInstaller --clean build_windows.spec
```

## Distribution

The `ScreensaverApp.exe` in the `dist/` folder is standalone and can be:
- Copied to any Windows machine (no Python required)
- Shared with others
- Installed in Program Files

## Alternative: cx_Freeze

If PyInstaller doesn't work, try cx_Freeze:

1. Install: `pip install cx_Freeze`
2. Create `setup.py`:
```python
from cx_Freeze import setup, Executable

setup(
    name="ScreensaverApp",
    version="1.0",
    description="Screensaver Application",
    executables=[Executable("main.py", base="Win32GUI", target_name="ScreensaverApp.exe")]
)
```
3. Build: `python setup.py build`
