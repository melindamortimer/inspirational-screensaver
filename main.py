"""
Main application window for the screensaver selector and preview.
"""

import tkinter as tk
from tkinter import ttk
from screensaver_base import ScreensaverRegistry
# Import all screensaver implementations to register them
import color_wheel_screensaver


class ScreensaverApp:
    """
    Main application window with screensaver preview and controls.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Screensaver Selector")
        self.root.geometry("800x600")

        # Current screensaver instance
        self.current_screensaver = None
        self.fullscreen_window = None

        # Get all registered screensavers
        self.screensaver_classes = ScreensaverRegistry.get_all()

        # Setup UI
        self._create_ui()

        # Select first screensaver by default
        if self.screensaver_classes:
            self.screensaver_selector.current(0)
            self._on_screensaver_change(None)

    def _create_ui(self):
        """Create the main UI layout."""
        # Top control panel
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Screensaver selector dropdown
        ttk.Label(control_frame, text="Select Screensaver:").pack(side=tk.LEFT, padx=(0, 10))

        screensaver_names = [cls(None).get_name() for cls in self.screensaver_classes]
        self.screensaver_selector = ttk.Combobox(
            control_frame,
            values=screensaver_names,
            state="readonly",
            width=30
        )
        self.screensaver_selector.pack(side=tk.LEFT, padx=(0, 20))
        self.screensaver_selector.bind("<<ComboboxSelected>>", self._on_screensaver_change)

        # Start button
        self.start_button = ttk.Button(
            control_frame,
            text="Start Fullscreen",
            command=self._start_fullscreen
        )
        self.start_button.pack(side=tk.LEFT)

        # Preview area
        preview_frame = ttk.Frame(self.root, padding="10")
        preview_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        ttk.Label(preview_frame, text="Preview:", font=("Arial", 10, "bold")).pack(anchor=tk.W)

        # Canvas for screensaver preview
        self.preview_canvas = tk.Canvas(
            preview_frame,
            bg="black",
            highlightthickness=1,
            highlightbackground="gray"
        )
        self.preview_canvas.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

    def _on_screensaver_change(self, event):
        """Handle screensaver selection change."""
        # Stop and cleanup current screensaver
        if self.current_screensaver:
            self.current_screensaver.cleanup()

        # Get selected screensaver class
        selected_index = self.screensaver_selector.current()
        if selected_index >= 0:
            screensaver_class = self.screensaver_classes[selected_index]

            # Create new instance with preview canvas
            self.current_screensaver = screensaver_class(self.preview_canvas)

            # Start preview animation
            self.current_screensaver.start()

    def _start_fullscreen(self):
        """Launch the selected screensaver in fullscreen mode."""
        if not self.current_screensaver:
            return

        # Create fullscreen window
        self.fullscreen_window = tk.Toplevel(self.root)
        self.fullscreen_window.attributes("-fullscreen", True)
        self.fullscreen_window.configure(bg="black")

        # Create canvas for fullscreen screensaver
        fullscreen_canvas = tk.Canvas(
            self.fullscreen_window,
            bg="black",
            highlightthickness=0
        )
        fullscreen_canvas.pack(fill=tk.BOTH, expand=True)

        # Create new instance of selected screensaver for fullscreen
        selected_index = self.screensaver_selector.current()
        screensaver_class = self.screensaver_classes[selected_index]
        fullscreen_screensaver = screensaver_class(fullscreen_canvas)

        # Start fullscreen screensaver
        fullscreen_screensaver.start()

        # Bind escape key to exit fullscreen
        def exit_fullscreen(event=None):
            fullscreen_screensaver.cleanup()
            self.fullscreen_window.destroy()
            self.fullscreen_window = None

        self.fullscreen_window.bind("<Escape>", exit_fullscreen)
        self.fullscreen_window.bind("<Button-1>", exit_fullscreen)  # Click to exit

        # Show instruction label
        info_label = tk.Label(
            self.fullscreen_window,
            text="Press ESC or click to exit",
            fg="white",
            bg="black",
            font=("Arial", 12)
        )
        info_label.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

        # Fade out instruction after 3 seconds
        self.fullscreen_window.after(3000, info_label.destroy)

    def run(self):
        """Start the application main loop."""
        self.root.mainloop()


def main():
    """Entry point for the application."""
    root = tk.Tk()
    app = ScreensaverApp(root)
    app.run()


if __name__ == "__main__":
    main()
