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

    def get_name(self) -> str:
        return "Color Wheel"

    def render(self):
        """Render the current color as a fullscreen rectangle."""
        # Convert HSV to RGB
        # HSV: Hue (0-1), Saturation (1 = full color), Value (1 = full brightness)
        rgb = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)

        # Convert to hex color for Tkinter
        r = int(rgb[0] * 255)
        g = int(rgb[1] * 255)
        b = int(rgb[2] * 255)
        color = f"#{r:02x}{g:02x}{b:02x}"

        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Fill the entire canvas with the current color
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            0, 0, width, height,
            fill=color,
            outline=color
        )

        # Increment hue for next frame
        self.hue += self.hue_speed
        if self.hue >= 1.0:
            self.hue = 0.0  # Wrap around after completing the color wheel
