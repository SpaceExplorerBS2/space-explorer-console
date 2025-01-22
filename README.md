# space-explorer-console

A simple console game written in Python.

## How to Run

1. Set up a virtual environment:
    ```sh
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    venv\Scripts\Activate.ps1
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the Flask application:
    ```sh
    python main.py
    ```

4. Run the UniCursed console game:
    ```sh
    python game.py
    ```

5. Sample Data
    - Ensure [planets.json](http://_vscodecontentref_/5) is in the project directory with the sample data.

## Controls for UniCursed Console Game

- Use the arrow keys to move the character (`@`).
- Press `q` to quit the game.