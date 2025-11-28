# Stealth Game (Refactored)

A Python-based text adventure engine demonstrating modern software architecture principles. This project refactors a legacy procedural script into a modular, object-oriented application with external configuration and state persistence.

## 🏗 Architectural Features

* **Object-Oriented Design:** Game logic is decoupled from state management using `StealthGame` and `Scenario` classes.
* **Data-Driven Content:** All game text and scoring logic are loaded from an external `scenarios.json` file, adhering to the Separation of Concerns principle.
* **State Serialization:** Implements a JSON-based Save/Load system to persist player progress (`savegame.json`).
* **Type Safety:** Utilizes Python 3.11 `dataclasses` and strict type hinting for maintainability.
* **Unit Testing:** Includes a `unittest` suite to validate scoring algorithms and logic modifiers.
* **Portable Build:** Compiled via PyInstaller into a standalone executable with bundled resources.

## 🚀 How to Play

1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/BrandonMaloneySEO/stealth_game.git](https://github.com/BrandonMaloneySEO/stealth_game.git)
    ```
2.  **Run the source:**
    ```bash
    python3 game.py
    ```
3.  **Or run the tests:**
    ```bash
    python3 test_game.py
    ```

## 🛠 Tech Stack

* Python 3.11
* PyInstaller (for binary compilation)
* Unittest (for logic validation)
