import unittest
from unittest.mock import patch, MagicMock
import pygame
import pygame.time
from display import Display
from constants import RgbColors, GameSettings, Point
from snake import Snake


class TestDisplay(unittest.TestCase):

    def setUp(self):
        self.display = Display()
        self.snake = Snake()
        self.display.width = 640
        self.display.height = 480

    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.font.Font")
    @patch("pygame.time.Clock")
    def test_init(
        self, mock_clock, mock_font, mock_set_caption, mock_set_mode, mock_init
    ):
        display = Display()
        mock_init.assert_called_once()
        mock_font.assert_called_once()
        mock_set_caption.assert_called_with("Snake")
        mock_set_mode.assert_called_with((GameSettings.WIDTH, GameSettings.HEIGHT))
        mock_clock.assert_called_once()

        self.assertIsInstance(display.font, MagicMock)
        self.assertIsInstance(display.window, MagicMock)
        self.assertIsInstance(display.clock, MagicMock)

    @patch('pygame.draw.rect')
    @patch('pygame.font.Font')
    @patch('pygame.display.flip')
    @patch('pygame.display.set_mode')
    def test_update_ui(self, mock_set_mode, mock_display_flip, mock_font, mock_draw_rect):
        """Test the UI is correctly updated with new snake, food, score and high score values."""
        mock_window = mock_set_mode.return_value
        mock_font_instance = mock_font.return_value
        mock_font_instance.render = MagicMock()

        self.food = Point(100, 100)
        self.score = 10
        self.display.window = mock_window
        self.display.font = mock_font_instance
        self.high_score = 100
        self.display.update_ui(self.snake, self.food, self.score, self.high_score)

        mock_draw_rect.assert_called()
        mock_font_instance.render.assert_called()
        mock_display_flip.assert_called()

    @patch("pygame.draw.rect")
    def test_draw_snake(self, mock_draw_rect):
        """Test that the rendering of the snake is in the correct style."""
        snake = MagicMock()
        snake.blocks = [Point(0, 0), Point(GameSettings.BLOCK_SIZE, 0), Point(2 * GameSettings.BLOCK_SIZE, 0)]
        self.display.draw_snake(snake)

        mock_draw_rect.assert_any_call(
            self.display.window,
            RgbColors.BLUE1,
            pygame.Rect(0, 0, GameSettings.BLOCK_SIZE, GameSettings.BLOCK_SIZE),
        )
        mock_draw_rect.assert_any_call(
            self.display.window, RgbColors.BLUE2, pygame.Rect(4, 4, 12, 12)
        )

    @patch("pygame.draw.rect")
    def test_draw_food(self, mock_draw_rect):
        """Test that the rendering of the food is in the correct style."""
        food = Point(0, 0)
        self.display.draw_food(food)

        mock_draw_rect.assert_called_once_with(
            self.display.window,
            RgbColors.RED,
            pygame.Rect(0, 0, GameSettings.BLOCK_SIZE, GameSettings.BLOCK_SIZE),
        )

    @patch("pygame.font.Font")
    def test_draw_score(self, mock_font):
        """Test for the correct rendering of the score."""
        score = 10
        mock_font_instance = mock_font.return_value
        mock_render = MagicMock()
        mock_font_instance.render.return_value = mock_render
        mock_render.get_width.return_value = 160
        mock_render.get_height.return_value = 120
        mock_window_surface = MagicMock()
        self.display.window = mock_window_surface
        self.display.font = mock_font_instance
        self.display.draw_score(score)

        mock_font_instance.render.assert_called_once()
        mock_window_surface.blit.assert_called_once()

    @patch("pygame.display.flip")
    @patch("pygame.font.Font")
    def test_render_game_over(self, mock_font, mock_flip):
        """Test for the correct rendering of Game Over."""
        mock_font_instance = mock_font.return_value
        mock_render = MagicMock()
        mock_font_instance.render.return_value = mock_render
        mock_render.get_width.return_value = 160
        mock_render.get_height.return_value = 120
        mock_window_surface = MagicMock()
        self.display.window = mock_window_surface
        self.display.render_game_over()

        mock_font_instance.render.assert_called_once()
        mock_window_surface.blit.assert_called_once()
        mock_flip.assert_called_once()

    @patch("pygame.display.flip")
    @patch("pygame.font.Font")
    def test_render_play_again(self, mock_font, mock_flip):
        """Test for the correct rendering of Play Again prompt."""
        mock_font_instance = mock_font.return_value
        mock_render = MagicMock()
        mock_font_instance.render.return_value = mock_render
        mock_render.get_rect.return_value = pygame.Rect(0, 0, 100, 50)
        mock_window_surface = MagicMock()
        self.display.window = mock_window_surface
        self.display.render_play_again()

        mock_font_instance.render.assert_called_once()
        mock_window_surface.blit.assert_called_once()
        mock_flip.assert_called_once()

    @patch("pygame.font.Font")
    def test_render_high_score(self, mock_font):
        """Test for correct rendering of high score."""
        high_score = 100
        mock_font_instance = mock_font.return_value
        mock_render = MagicMock()
        mock_font_instance.render.return_value = mock_render
        mock_render.get_width.return_value = 160
        mock_render.get_height.return_value = 120
        mock_window_surface = MagicMock()
        self.display.window = mock_window_surface
        self.display.font = mock_font_instance
        self.display.draw_score(high_score)

        mock_font_instance.render.assert_called_once()
        mock_window_surface.blit.assert_called_once()

    @patch("pygame.display.flip")
    @patch("pygame.font.Font")
    def test_render_new_high_score(self, mock_font, mock_flip):
        """Test for correct rendering of new high score."""
        mock_font_instance = mock_font.return_value
        mock_render = MagicMock()
        mock_font_instance.render.return_value = mock_render
        mock_render.get_rect.return_value = pygame.Rect(0, 0, 100, 50)
        mock_window_surface = MagicMock()
        self.display.window = mock_window_surface
        self.display.render_play_again()

        mock_font_instance.render.assert_called_once()
        mock_window_surface.blit.assert_called_once()
        mock_flip.assert_called_once()


if __name__ == "__main__":
    unittest.main()
