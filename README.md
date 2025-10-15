# Inspirational Screensaver

A customizable screensaver application with a windowed preview and multiple screensaver types.

## Features

- Windowed preview mode to see screensavers before launching
- Dropdown selector to choose between different screensaver types
- Fullscreen mode with easy exit (ESC key or click)
- Extensible architecture for adding new screensaver types

## Current Screensavers

1. **Color Wheel** - Continuously cycles through the color spectrum with a solid color fill

## Future Screensavers

- **Inspirational Quotes** - Display rotating inspirational quotes (planned)

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)

## Running the Application

```bash
python main.py
```

## Usage

1. Launch the application with `python main.py`
2. Select a screensaver type from the dropdown menu
3. View the preview in the main window
4. Click "Start Fullscreen" to launch in fullscreen mode
5. Press ESC or click anywhere to exit fullscreen

## Adding New Screensavers

To add a new screensaver type:

1. Create a new Python file (e.g., `my_screensaver.py`)
2. Import the base classes:
   ```python
   from screensaver_base import ScreensaverBase, ScreensaverRegistry
   ```
3. Create a class that inherits from `ScreensaverBase` and decorate it with `@ScreensaverRegistry.register`:
   ```python
   @ScreensaverRegistry.register
   class MyScreensaver(ScreensaverBase):
       def get_name(self) -> str:
           return "My Screensaver"

       def render(self):
           # Draw your screensaver on self.canvas
           pass
   ```
4. Import your screensaver in [main.py](main.py) (add to imports at the top):
   ```python
   import my_screensaver
   ```

The new screensaver will automatically appear in the dropdown selector.

## Architecture

- [screensaver_base.py](screensaver_base.py) - Base class and registry system
- [color_wheel_screensaver.py](color_wheel_screensaver.py) - Color wheel implementation
- [main.py](main.py) - Main application window and controls

The application uses a plugin-style architecture where screensavers register themselves with the `ScreensaverRegistry`. This makes it easy to add new screensaver types without modifying existing code.
