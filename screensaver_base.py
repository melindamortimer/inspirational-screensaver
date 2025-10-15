"""
Base screensaver interface for the screensaver application.
All screensaver implementations should inherit from this class.
"""

from abc import ABC, abstractmethod
import tkinter as tk


class ScreensaverBase(ABC):
    """
    Abstract base class for all screensaver implementations.

    Each screensaver must implement the render method to draw its content
    on the provided canvas.
    """

    def __init__(self, canvas: tk.Canvas):
        """
        Initialize the screensaver with a canvas to draw on.

        Args:
            canvas: The Tkinter canvas to render the screensaver on
        """
        self.canvas = canvas
        self.is_running = False
        self.animation_id = None

    @abstractmethod
    def get_name(self) -> str:
        """
        Return the display name of this screensaver.

        Returns:
            String name to show in the screensaver selector
        """
        pass

    @abstractmethod
    def render(self):
        """
        Render one frame of the screensaver on the canvas.
        This method is called repeatedly to animate the screensaver.
        """
        pass

    def start(self):
        """Start the screensaver animation."""
        if not self.is_running:
            self.is_running = True
            self._animate()

    def stop(self):
        """Stop the screensaver animation."""
        self.is_running = False
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
            self.animation_id = None

    def cleanup(self):
        """Clean up resources before switching screensavers."""
        self.stop()
        self.canvas.delete("all")

    def _animate(self):
        """Internal animation loop."""
        if self.is_running:
            self.render()
            # Schedule next frame (approximately 15 FPS for efficiency)
            self.animation_id = self.canvas.after(67, self._animate)


class ScreensaverRegistry:
    """
    Registry to manage available screensaver types.
    Screensavers register themselves here to be discovered by the main application.
    """

    _screensavers = []

    @classmethod
    def register(cls, screensaver_class):
        """
        Register a screensaver class.

        Args:
            screensaver_class: A class that inherits from ScreensaverBase
        """
        if not issubclass(screensaver_class, ScreensaverBase):
            raise ValueError(f"{screensaver_class} must inherit from ScreensaverBase")
        cls._screensavers.append(screensaver_class)
        return screensaver_class

    @classmethod
    def get_all(cls):
        """
        Get all registered screensaver classes.

        Returns:
            List of screensaver classes
        """
        return cls._screensavers.copy()

    @classmethod
    def clear(cls):
        """Clear all registered screensavers (useful for testing)."""
        cls._screensavers.clear()
