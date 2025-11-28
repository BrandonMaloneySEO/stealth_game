import sys
import os
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

@dataclass
class Option:
    text: str
    player_points: int
    guard_points: int

@dataclass
class Scenario:
    prompt: str
    options: List[Option]

class StealthGame:
    def __init__(self):
        self.player_score: int = 0
        self.guard_alert: int = 0
        self.history: List[int] = [] 
        self.current_idx: int = 0 
        
        # Configuration consts
        self.WIN_THRESHOLD = 25
        self.LOSE_THRESHOLD = 20
        self.INSTANT_FAIL = 100
        self.save_file = Path("savegame.json")
        
        # LOAD CONTENT
        self.scenarios: List[Scenario] = self._load_scenarios()

    def _get_resource_path(self, relative_path: str) -> Path:
        """
        ARCHITECTURAL FIX: 
        Locates files whether running as a script or a frozen executable.
        PyInstaller unpacks data to sys._MEIPASS.
        """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return Path(base_path) / relative_path

    def _load_scenarios(self) -> List[Scenario]:
        # Use the helper to find the file correctly
        file_path = self._get_resource_path("scenarios.json")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            loaded_scenarios = []
            for item in data:
                options_list = [
                    Option(opt["text"], opt["player_points"], opt["guard_points"]) 
                    for opt in item["options"]
                ]
                loaded_scenarios.append(Scenario(item["prompt"], options_list))
            return loaded_scenarios
        except FileNotFoundError:
            print(f">> CRITICAL ERROR: Could not find config at {file_path}")
            input("Press Enter to exit...") # Keeps window open so user sees error
            sys.exit(1)

    def save_game(self):
        state_data = {
            "player_score": self.player_score,
            "guard_alert": self.guard_alert,
            "history": self.history,
            "current_idx": self.current_idx
        }
        with open(self.save_file, "w") as f:
            json.dump(state_data, f)
        print("\n>> GAME SAVED SUCCESSFULLY. Goodbye!")
        sys.exit(0)

    def load_game(self):
        if not self.save_file.exists():
            print("\n>> No save file found! Starting new game...")
            return

        with open(self.save_file, "r") as f:
            state_data = json.load(f)
        
        self.player_score = state_data["player_score"]
        self.guard_alert = state_data["guard_alert"]
        self.history = state_data["history"]
        self.current_idx = state_data["current_idx"]
        print(f"\n>> Save loaded! Resuming at Scenario {self.current_idx + 1}...")

    def _get_valid_input(self, num_options: int) -> int:
        while True:
            user_input = input(f"\nSelect option (1-{num_options}) or 'S' to Save & Quit: ").strip().upper()
            
            if user_input == 'S':
                self.save_game() 
            
            try:
                choice = int(user_input)
                if 1 <= choice <= num_options:
                    return choice - 1
                print(f"Invalid input. Please enter 1-{num_options} or 'S'.")
            except ValueError:
                print("Invalid input.")

    def _apply_logic_modifiers(self, choice_idx: int):
        if choice_idx == 1:
            consecutive_hides = 0
            for past_choice in reversed(self.history):
                if past_choice == 1:
                    consecutive_hides += 1
                else:
                    break
            if consecutive_hides >= 3:
                print(">> The guard gets suspicious of the silent museum. Alert rises!")
                self.guard_alert += 100

        if choice_idx == 0 and len(self.history) >= 2:
             if self.history[-1] == 0 and self.history[-2] == 0:
                 self.player_score += 1 

    def start_menu(self):
        print("~~ A THIEF IN THE NIGHT ~~")
        print("1. New Game")
        print("2. Load Game")
        choice = input("\nChoose: ")
        
        if choice == "2":
            self.load_game()
        else:
            print("\n>> Starting new game...")

    def play(self):
        self.start_menu()
        while self.current_idx < len(self.scenarios):
            scenario = self.scenarios[self.current_idx]
            
            print(f"\n--- SCENARIO {self.current_idx + 1} ---")
            print(f"[Score: {self.player_score} | Alert: {self.guard_alert}]")
            print(scenario.prompt)
            
            for idx, opt in enumerate(scenario.options):
                print(f"{idx + 1}) {opt.text}")

            choice_idx = self._get_valid_input(len(scenario.options))
            selected_opt = scenario.options[choice_idx]

            self.player_score += selected_opt.player_points
            self.guard_alert += selected_opt.guard_points
            
            self._apply_logic_modifiers(choice_idx)
            self.history.append(choice_idx)

            if self.guard_alert >= self.INSTANT_FAIL:
                print("\nGuard: 'Halt! You're under arrest!'")
                input("Press Enter to exit...")
                return
            if self.player_score == 0 and self.guard_alert > self.LOSE_THRESHOLD:
                print("\nGuard: 'If you stay here longer, you'll become an exhibit!'")
                input("Press Enter to exit...")
                return

            self.current_idx += 1

        self._conclude_game()

    def _conclude_game(self):
        print("\n--- FINAL REPORT ---")
        print(f"Player Progress: {self.player_score}/{self.WIN_THRESHOLD}")
        print(f"Guard Alert: {self.guard_alert}/{self.LOSE_THRESHOLD}")
        
        if self.player_score >= self.WIN_THRESHOLD and self.guard_alert <= self.LOSE_THRESHOLD:
            print("RESULT: SUCCESS!")
        elif self.player_score >= self.WIN_THRESHOLD:
            print("RESULT: CAUGHT!")
        else:
            print("RESULT: FAILED.")
        
        if self.save_file.exists():
            self.save_file.unlink()
        input("Press Enter to exit...")

if __name__ == "__main__":
    game = StealthGame()
    game.play()