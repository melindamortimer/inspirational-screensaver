"""
Color Wheel Screensaver - displays a solid color that rotates through the color wheel.
"""

import colorsys
from screensaver_base import ScreensaverBase, ScreensaverRegistry


@ScreensaverRegistry.register
class ColorWheelScreensaver(ScreensaverBase):
    """
    A screensaver that fills the screen with a solid color,
    continuously cycling through the HSV color wheel.
    """

    def __init__(self, canvas):
        super().__init__(canvas)
        self.hue = 0.0  # Start at red (0 degrees on color wheel)
        self.hue_speed = 0.001  # Speed of color rotation (adjust for faster/slower)
        self.color_rect = None  # Reusable rectangle object

    def get_name(self) -> str:
        return "Color Wheel"

    def render(self):
        """Render the current color using a reusable rectangle object."""
        if not self.canvas:
            return

        # Convert HSV to RGB
        # HSV: Hue (0-1), Saturation (1 = full color), Value (1 = full brightness)
        rgb = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)

        # Convert to hex color for Tkinter
        r = int(rgb[0] * 255)
        g = int(rgb[1] * 255)
        b = int(rgb[2] * 255)
        color = f"#{r:02x}{g:02x}{b:02x}"

        try:
            # Get canvas dimensions
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()

            # Create rectangle on first render, reuse it afterwards
            if self.color_rect is None:
                self.color_rect = self.canvas.create_rectangle(
                    0, 0, width, height,
                    fill=color,
                    outline=color,
                    tags="color_bg"
                )
            else:
                # Just update the color of existing rectangle
                self.canvas.itemconfig(self.color_rect, fill=color, outline=color)
                # Update coordinates in case window was resized
                self.canvas.coords(self.color_rect, 0, 0, width, height)
        except:
            pass  # Canvas may not be fully initialized yet

        # Increment hue for next frame and wrap around
        self.hue = (self.hue + self.hue_speed) % 1.0
