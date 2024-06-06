import io
import unittest
from unittest.mock import patch, MagicMock, mock_open
import pygame
from game import Game
from constants import GameSettings, Point
from snake import Snake


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_init(self):
        """Test the initialization of the Game object."""
        self.assertIsNotNone(self.game.display)
        self.assertIsNotNone(self.game.snake)
        self.assertEqual(self.game.score, 0)
        self.assertIsNotNone(self.game.food)

    def test_is_collision(self):
        """Test if the snake is out of the window boundary or collides with itself."""
        # Snake is out of bounds
        self.game.snake.head = Point(-1, -1)
        self.assertTrue(self.game.is_collision())
        # Snake collides with itself
        self.game.snake.head = self.game.snake.blocks[1]
        self.assertTrue(self.game.is_collision())

    @patch('pygame.event.get')
    @patch('pygame.draw.rect')
    @patch('pygame.display.flip')
    @patch('pygame.font.Font')
    def test_play_step(self, mock_font, mock_display_flip, mock_draw_rect, mock_event_get):
        """Test that a step through the game correctly updates the snake, food and score."""
        mock_event_get.return_value = []
        mock_font_instance = MagicMock()
        self.game.display.window = MagicMock(spec=pygame.Surface)
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_font_instance.render.return_value = mock_surface
        mock_font.return_value = mock_font_instance

        init_snake_length = len(self.game.snake.blocks)
        init_score = self.game.score
        init_head_position = self.game.snake.head
        # Place food in front of snake
        self.game.food = Point(
            init_head_position.x + GameSettings.BLOCK_SIZE, init_head_position.y
        )
        self.game.play_step()

        self.assertEqual(len(self.game.snake.blocks), init_snake_length + 1)
        self.assertEqual(self.game.score, init_score + 1)
        # Check snake head is one block in front of the initial head position
        new_head_position = Point(
            init_head_position.x + GameSettings.BLOCK_SIZE, init_head_position.y
        )
        self.assertEqual(self.game.snake.head, new_head_position)

    def test_place_food(self):
        """Test that food is not placed in the snake's position."""
        self.game.place_food()
        self.assertNotIn(self.game.food, self.game.snake.blocks)

    @patch("pygame.event.get")
    def test_play_again_y(self, mock_event_get):
        """Test that the play_again method returns True when y key is pressed."""
        mock_event_get.return_value = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_y)]
        value = self.game.play_again()
        self.assertTrue(value)

    @patch("pygame.event.get")
    def test_play_again_return(self, mock_event_get):
        """Test that the play_again method returns True when Return key is pressed."""
        mock_event_get.return_value = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_RETURN)]
        value = self.game.play_again()
        self.assertTrue(value)

    @patch("pygame.event.get")
    def test_play_again_n(self, mock_event_get):
        """Test that the play_again method returns True when n key is pressed."""
        mock_event_get.return_value = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_n)]
        value = self.game.play_again()
        self.assertFalse(value)

    @patch("pygame.event.get")
    def test_play_again_esc(self, mock_event_get):
        """Test that the play_again method returns True when Esc key is pressed."""
        mock_event_get.return_value = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)]
        value = self.game.play_again()
        self.assertFalse(value)

    def test_restart_game(self):
        """Test that the restart_game method initializes the Game with initial default attributes."""
        self.game.snake = Snake(init_length=10)
        self.game.score = 10
        init_high_score = self.game.high_score

        self.game.restart_game()
        self.assertEqual(len(self.game.snake.blocks), 3)
        self.assertEqual(self.game.score, 0)
        self.assertIsNotNone(self.game.food)
        self.assertEqual(init_high_score, self.game.high_score)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_high_score_no_json_file(self, mock_open):
        """Test that the high score is 0 when no json file is provided."""
        returned_high_score = self.game.load_high_score()
        self.assertEqual(returned_high_score, 0)

    @patch("builtins.open", return_value=io.StringIO('{"high_score": 100}'))
    def test_load_high_score_existing_file(self, mock_open):
        """Test that the load_high_score method correctly retrieves the value of the high score from the json file."""
        returned_high_score = self.game.load_high_score()
        self.assertEqual(returned_high_score, 100)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("json.load", return_value={"high_score": 100})
    def test_update_high_score(self, mock_load, mock_dump, mock_open):
        """Test that the json file is read and updates the json file with the new high score."""
        mock_file = mock_open.return_value
        mock_file.__enter__.return_value = mock_file

        self.game.update_high_score(200)

        # Check file is opened in read-mode for loading high score, and opened in write-mode for updating high score
        mock_open.assert_any_call("high_score.json", "r")
        mock_open.assert_any_call("high_score.json", "w")

        mock_dump.assert_called_with({"high_score": 200}, mock_file)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('json.load', return_value={"high_score": 100})
    def test_update_high_score_with_score_lower_than_high_score(self, mock_load, mock_dump, mock_open):
        """Test that the high score remains unchanged for a score less than the current high score."""
        mock_file = mock_open.return_value
        mock_file.__enter__.return_value = mock_file

        self.game.update_high_score(50)

        # Check high score is not changed
        mock_open.assert_called_once_with("high_score.json", "r")
        mock_dump.assert_not_called()


if __name__ == "__main__":
    unittest.main()
