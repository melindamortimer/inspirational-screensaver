"""
Inspirational Quotes Screensaver - displays inspirational quotes with fade in/out effects.
"""

import random
import os
import math
from screensaver_base import ScreensaverBase, ScreensaverRegistry


@ScreensaverRegistry.register
class InspirationalQuotesScreensaver(ScreensaverBase):
    """
    A screensaver that displays inspirational quotes with smooth fade in/out transitions.
    Quotes are loaded from quotes.txt file (format: quote|author per line).
    Features: horizontal drift, background shadow, subtle scale pulsing.
    """

    # Timing configuration (in milliseconds)
    DISPLAY_DURATION_TEST = 7000  # 7 seconds for testing
    DISPLAY_DURATION_PROD = 1800000  # 30 minutes for production
    FADE_DURATION = 2000  # 2 seconds for fade in/out
    FADE_STEPS = 60  # Number of steps in fade animation (smoother with more steps)

    # Animation configuration
    DRIFT_SPEED_BASE = 0.05  # Base pixels per frame for horizontal drift (extremely subtle)
    SHADOW_DRIFT_MULTIPLIER = 0.7  # Shadow drifts at 70% speed of main text
    RANDOM_START_RANGE = 100  # Random offset range for starting position (pixels)

    def __init__(self, canvas, use_test_timing=False):
        """
        Initialize the inspirational quotes screensaver.

        Args:
            canvas: The Tkinter canvas to render on
            use_test_timing: If True, use 7s timing; if False, use 30min timing
        """
        super().__init__(canvas)
        self.quotes = []
        self.current_quote = None
        self.current_author = None
        self.last_quote_tuple = None  # Track last quote to prevent duplicates
        self.quote_text_id = None
        self.author_text_id = None
        self.shadow_quote_id = None  # Background shadow text
        self.shadow_author_id = None
        self.current_alpha = 0.0  # Current opacity (0.0 to 1.0)
        self.fade_state = "idle"  # States: idle, fading_in, displaying, fading_out
        self.fade_step = 0
        self.display_timer_id = None
        self.use_test_timing = use_test_timing

        # Animation state
        self.drift_offset = 0.0  # Current horizontal drift offset
        self.shadow_drift_offset = 0.0  # Shadow drift offset
        self.drift_speed = 0.0  # Current drift speed (randomized per quote)
        self.shadow_drift_speed = 0.0  # Shadow drift speed (opposite direction)
        self.frame_count = 0  # Track frames for animations
        self.random_start_x = 0  # Random horizontal start offset
        self.random_start_y = 0  # Random vertical start offset

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
        """Select a random quote from the list, ensuring it's different from the last one."""
        if not self.quotes:
            return

        # If we only have one quote, just use it
        if len(self.quotes) == 1:
            quote, author = self.quotes[0]
            self.current_quote = quote
            self.current_author = f"— {author}"
            self.last_quote_tuple = self.quotes[0]
            return

        # Select a quote that's different from the last one
        selected_quote = random.choice(self.quotes)

        # Keep trying until we get a different quote (max 10 attempts)
        attempts = 0
        while selected_quote == self.last_quote_tuple and attempts < 10:
            selected_quote = random.choice(self.quotes)
            attempts += 1

        quote, author = selected_quote
        self.current_quote = quote
        self.current_author = f"— {author}"
        self.last_quote_tuple = selected_quote

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
        """Create or update the text items on canvas with smooth drift and parallax animations."""
        if not self.canvas or not self.current_quote:
            return

        try:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            color = self._get_alpha_color(self.current_alpha)
            shadow_color = self._get_alpha_color(self.current_alpha * 0.15)  # Very faded shadow

            # Calculate font size based on canvas size
            quote_font_size = max(20, min(36, width // 30))
            author_font_size = max(16, min(28, width // 40))
            shadow_font_size = int(quote_font_size * 1.8)  # Shadow is larger

            # Calculate positions with drift and random starting position
            center_x = width // 2 + self.drift_offset + self.random_start_x
            center_y = height // 2 + self.random_start_y

            # Parallax: shadow drifts at different rate and offset for depth
            shadow_center_x = width // 2 + self.shadow_drift_offset + (self.random_start_x * 0.7)
            shadow_center_y = height // 2 + (self.random_start_y * 0.7)

            # Create text items if they don't exist
            if self.quote_text_id is None:
                # Background shadow (larger, very faded, drifts opposite direction)
                self.shadow_quote_id = self.canvas.create_text(
                    shadow_center_x,
                    shadow_center_y,
                    text=self.current_quote,
                    fill=shadow_color,
                    font=("Arial", shadow_font_size, "bold"),
                    width=width * 0.9,
                    justify="center",
                    tags="shadow"
                )

                # Main quote text (centered, with wrapping, with drift and wave)
                self.quote_text_id = self.canvas.create_text(
                    center_x,
                    center_y,
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
                    author_y = center_y + 60

                # Author text (below quote)
                self.author_text_id = self.canvas.create_text(
                    center_x,
                    author_y,
                    text=self.current_author,
                    fill=color,
                    font=("Arial", author_font_size, "italic"),
                    justify="center",
                    tags="author"
                )
            else:
                # Update shadow with parallax
                if self.shadow_quote_id:
                    self.canvas.itemconfig(self.shadow_quote_id,
                                          fill=shadow_color,
                                          font=("Arial", shadow_font_size, "bold"),
                                          width=width * 0.9)
                    self.canvas.coords(self.shadow_quote_id, shadow_center_x, shadow_center_y)

                # Update existing text color and font (in case of resize)
                self.canvas.itemconfig(self.quote_text_id,
                                      fill=color,
                                      font=("Arial", quote_font_size, "bold"),
                                      width=width * 0.8)
                self.canvas.itemconfig(self.author_text_id,
                                      fill=color,
                                      font=("Arial", author_font_size, "italic"))

                # Update position with drift and wave
                self.canvas.coords(self.quote_text_id, center_x, center_y)

                # Recalculate author position based on quote height
                quote_bbox = self.canvas.bbox(self.quote_text_id)
                if quote_bbox:
                    author_y = quote_bbox[3] + 40
                else:
                    author_y = center_y + 60

                self.canvas.coords(self.author_text_id, center_x, author_y)

        except Exception as e:
            pass  # Canvas may not be ready

    def _start_fade_in(self):
        """Start the fade-in animation with random starting position and drift direction."""
        self.fade_state = "fading_in"
        self.fade_step = 0
        self.current_alpha = 0.0
        # Reset drift to start from center
        self.drift_offset = 0.0
        self.shadow_drift_offset = 0.0
        # Random starting position (within range)
        self.random_start_x = random.uniform(-self.RANDOM_START_RANGE, self.RANDOM_START_RANGE)
        self.random_start_y = random.uniform(-self.RANDOM_START_RANGE // 2, self.RANDOM_START_RANGE // 2)
        # Randomize drift direction: 50% chance left, 50% chance right
        drift_direction = random.choice([-1, 1])
        self.drift_speed = self.DRIFT_SPEED_BASE * drift_direction
        # Shadow drifts opposite direction at 70% speed
        self.shadow_drift_speed = -self.drift_speed * self.SHADOW_DRIFT_MULTIPLIER

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
        if self.shadow_quote_id:
            self.canvas.delete(self.shadow_quote_id)
            self.shadow_quote_id = None
        if self.quote_text_id:
            self.canvas.delete(self.quote_text_id)
            self.quote_text_id = None
        if self.author_text_id:
            self.canvas.delete(self.author_text_id)
            self.author_text_id = None

    def _update_animations(self):
        """Update continuous animations - smooth horizontal drift."""
        # Update horizontal drift using randomized speeds (wraps around screen)
        self.drift_offset += self.drift_speed
        self.shadow_drift_offset += self.shadow_drift_speed

        # Wrap drift around screen (prevents it from drifting too far)
        if self.canvas:
            width = self.canvas.winfo_width()
            if abs(self.drift_offset) > width:
                self.drift_offset = 0
            if abs(self.shadow_drift_offset) > width:
                self.shadow_drift_offset = 0

        # Increment frame counter
        self.frame_count += 1

    def render(self):
        """Render one frame of the screensaver."""
        if not self.canvas:
            return

        # Update fade animation
        if self.fade_state in ["fading_in", "fading_out"]:
            self._update_fade()

        # Update continuous animations (drift, pulse)
        if self.fade_state != "idle":
            self._update_animations()

        # Create or update text with current alpha and animation state
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
