import unittest
from io import StringIO
from unittest.mock import patch
from game import StealthGame, Option, Scenario

class TestStealthGame(unittest.TestCase):

    def setUp(self):
        self.game = StealthGame()
        
        # Mock scenarios to isolate logic from external JSON
        self.game.scenarios = [
            Scenario("Test Scenario", [
                Option("Walk", 4, 4),      # Index 0
                Option("Hide", 0, 0),      # Index 1
                Option("Sneak", 2, 1)      # Index 2
            ])
        ]

    def test_initial_state(self):
        self.assertEqual(self.game.player_score, 0)
        self.assertEqual(self.game.guard_alert, 0)
        self.assertEqual(self.game.history, [])

    def test_basic_scoring(self):
        choice_idx = 0
        selected_opt = self.game.scenarios[0].options[choice_idx]
        
        self.game.player_score += selected_opt.player_points
        self.game.guard_alert += selected_opt.guard_points
        
        self.assertEqual(self.game.player_score, 4, "Player score should increase by 4")
        self.assertEqual(self.game.guard_alert, 4, "Guard alert should increase by 4")

    def test_hiding_penalty_logic(self):
        self.game.guard_alert = 0
        self.game.history = [1, 1, 1] 
        
        self.game._apply_logic_modifiers(1)
        
        self.assertEqual(self.game.guard_alert, 100, "Guard alert should spike to 100 after excessive hiding")

    def test_speed_run_bonus(self):
        self.game.player_score = 10
        self.game.history = [0, 0] 
        
        self.game._apply_logic_modifiers(0)
        
        self.assertEqual(self.game.player_score, 11, "Should receive +1 bonus for consistent walking")

if __name__ == '__main__':
    unittest.main()