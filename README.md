A desktop-based Hangman game built using Python and Tkinter, featuring a graphical user interface, score tracking, and a persistent leaderboard. The project demonstrates fundamental concepts of GUI design, event-driven programming, and file handling in Python.

Features:
  Interactive GUI: Built with Tkinter for smooth gameplay and user interaction.
  Score Tracking: Points are awarded for correct guesses, deducted for incorrect ones, and bonus points for completing a word.
  Persistent Leaderboard: Stores player names and scores using a JSON file that retains data between sessions.
  Modular Design: Organized codebase with separate modules for game logic, word selection, and hangman stages.
  Replay Option: Allows players to start a new game without restarting the application.

Technologies Used:
  Programming Language: Python
  GUI Framework: Tkinter
  Data Storage: JSON

How It Works:
  A random word is selected from a predefined list.
  Players guess one letter at a time.
  Incorrect guesses reduce the number of lives.
  Once the word is completed or lives run out, the player is prompted to enter their name, and the score is saved to the leaderboard.
