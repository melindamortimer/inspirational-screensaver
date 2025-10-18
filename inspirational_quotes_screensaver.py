"""
Inspirational Quotes Screensaver - displays inspirational quotes with fade in/out effects.
"""

import random
import os
from screensaver_base import ScreensaverBase, ScreensaverRegistry


@ScreensaverRegistry.register
class InspirationalQuotesScreensaver(ScreensaverBase):
    """
    A screensaver that displays inspirational quotes with smooth fade in/out transitions.
    Quotes are loaded from quotes.txt file (format: quote|author per line).
    """

    # Timing configuration (in milliseconds)
    DISPLAY_DURATION_TEST = 10000  # 10 seconds for testing
    DISPLAY_DURATION_PROD = 1800000  # 30 minutes for production
    FADE_DURATION = 2000  # 2 seconds for fade in/out
    FADE_STEPS = 60  # Number of steps in fade animation (smoother with more steps)

    def __init__(self, canvas, use_test_timing=True):
        """
        Initialize the inspirational quotes screensaver.

        Args:
            canvas: The Tkinter canvas to render on
            use_test_timing: If True, use 10s timing; if False, use 30min timing
        """
        super().__init__(canvas)
        self.quotes = []
        self.current_quote = None
        self.current_author = None
        self.quote_text_id = None
        self.author_text_id = None
        self.current_alpha = 0.0  # Current opacity (0.0 to 1.0)
        self.fade_state = "idle"  # States: idle, fading_in, displaying, fading_out
        self.fade_step = 0
        self.display_timer_id = None
        self.use_test_timing = use_test_timing

        # Load quotes from file
        self._load_quotes()

        # Select first random quote
        if self.quotes:
            self._select_random_quote()

    def get_name(self) -> str:
        return "Inspirational Quotes"

    def _load_quotes(self):
        """Load quotes from quotes.txt file."""
        quotes_file = os.path.join(os.path.dirname(__file__), "quotes.txt")

        if not os.path.exists(quotes_file):
            # Fallback quotes if file doesn't exist
            self.quotes = [
                ("The only way to do great work is to love what you do.", "Steve Jobs"),
                ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
                ("Success is not final, failure is not fatal.", "Winston Churchill"),
            ]
            return

        try:
            with open(quotes_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and '|' in line:
                        parts = line.split('|', 1)
                        if len(parts) == 2:
                            quote, author = parts
                            self.quotes.append((quote.strip(), author.strip()))
        except Exception as e:
            print(f"Error loading quotes: {e}")
            # Use fallback quotes
            self.quotes = [
                ("The only way to do great work is to love what you do.", "Steve Jobs"),
                ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
            ]

        # Shuffle quotes for random order
        random.shuffle(self.quotes)

    def _select_random_quote(self):
        """Select a random quote from the list."""
        if not self.quotes:
            return

        quote, author = random.choice(self.quotes)
        self.current_quote = quote
        self.current_author = f"— {author}"

    def _get_alpha_color(self, alpha):
        """
        Convert alpha value (0.0 to 1.0) to a color string for white text on black background.

        Args:
            alpha: Opacity from 0.0 (transparent) to 1.0 (fully visible)

        Returns:
            Hex color string (gray scale where 0.0 = black, 1.0 = white)
        """
        # For white text fading in/out, we go from black (0,0,0) to white (255,255,255)
        intensity = int(255 * alpha)
        return f"#{intensity:02x}{intensity:02x}{intensity:02x}"

    def _create_or_update_text(self):
        """Create or update the text items on canvas."""
        if not self.canvas or not self.current_quote:
            return

        try:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            color = self._get_alpha_color(self.current_alpha)

            # Calculate font size based on canvas size
            quote_font_size = max(20, min(36, width // 30))
            author_font_size = max(16, min(28, width // 40))

            # Create text items if they don't exist
            if self.quote_text_id is None:
                # Quote text (centered, with wrapping)
                self.quote_text_id = self.canvas.create_text(
                    width // 2,
                    height // 2,
                    text=self.current_quote,
                    fill=color,
                    font=("Arial", quote_font_size, "bold"),
                    width=width * 0.8,  # Wrap at 80% of canvas width
                    justify="center",
                    tags="quote"
                )

                # Get the bounding box of the quote to calculate author position
                quote_bbox = self.canvas.bbox(self.quote_text_id)
                if quote_bbox:
                    # Position author 40 pixels below the bottom of the quote
                    author_y = quote_bbox[3] + 40
                else:
                    # Fallback position
                    author_y = height // 2 + 60

                # Author text (below quote)
                self.author_text_id = self.canvas.create_text(
                    width // 2,
                    author_y,
                    text=self.current_author,
                    fill=color,
                    font=("Arial", author_font_size, "italic"),
                    justify="center",
                    tags="author"
                )
            else:
                # Update existing text color and font (in case of resize)
                self.canvas.itemconfig(self.quote_text_id,
                                      fill=color,
                                      font=("Arial", quote_font_size, "bold"),
                                      width=width * 0.8)
                self.canvas.itemconfig(self.author_text_id,
                                      fill=color,
                                      font=("Arial", author_font_size, "italic"))

                # Update position in case window was resized
                self.canvas.coords(self.quote_text_id, width // 2, height // 2)

                # Recalculate author position based on quote height
                quote_bbox = self.canvas.bbox(self.quote_text_id)
                if quote_bbox:
                    author_y = quote_bbox[3] + 40
                else:
                    author_y = height // 2 + 60

                self.canvas.coords(self.author_text_id, width // 2, author_y)

        except Exception as e:
            pass  # Canvas may not be ready

    def _start_fade_in(self):
        """Start the fade-in animation."""
        self.fade_state = "fading_in"
        self.fade_step = 0
        self.current_alpha = 0.0

    def _start_fade_out(self):
        """Start the fade-out animation."""
        self.fade_state = "fading_out"
        self.fade_step = 0
        self.current_alpha = 1.0

    def _update_fade(self):
        """Update the fade animation."""
        if self.fade_state == "fading_in":
            # Fade in: alpha goes from 0.0 to 1.0
            self.fade_step += 1
            self.current_alpha = min(1.0, self.fade_step / self.FADE_STEPS)

            if self.fade_step >= self.FADE_STEPS:
                # Fade in complete, start display timer
                self.fade_state = "displaying"
                self.current_alpha = 1.0
                self._schedule_fade_out()

        elif self.fade_state == "fading_out":
            # Fade out: alpha goes from 1.0 to 0.0
            self.fade_step += 1
            self.current_alpha = max(0.0, 1.0 - (self.fade_step / self.FADE_STEPS))

            if self.fade_step >= self.FADE_STEPS:
                # Fade out complete, select new quote and start fade in
                self.fade_state = "idle"
                self.current_alpha = 0.0
                self._select_random_quote()
                self._delete_text()
                self._start_fade_in()

    def _schedule_fade_out(self):
        """Schedule the fade-out animation after display duration."""
        if self.display_timer_id:
            self.canvas.after_cancel(self.display_timer_id)

        display_duration = self.DISPLAY_DURATION_TEST if self.use_test_timing else self.DISPLAY_DURATION_PROD
        self.display_timer_id = self.canvas.after(display_duration, self._start_fade_out)

    def _delete_text(self):
        """Delete text items from canvas."""
        if self.quote_text_id:
            self.canvas.delete(self.quote_text_id)
            self.quote_text_id = None
        if self.author_text_id:
            self.canvas.delete(self.author_text_id)
            self.author_text_id = None

    def render(self):
        """Render one frame of the screensaver."""
        if not self.canvas:
            return

        # Update fade animation
        if self.fade_state in ["fading_in", "fading_out"]:
            self._update_fade()

        # Create or update text with current alpha
        if self.fade_state != "idle":
            self._create_or_update_text()

    def start(self):
        """Start the screensaver animation."""
        super().start()
        if self.quotes:
            self._start_fade_in()

    def cleanup(self):
        """Clean up resources."""
        if self.display_timer_id:
            self.canvas.after_cancel(self.display_timer_id)
            self.display_timer_id = None
        self._delete_text()
        super().cleanup()
