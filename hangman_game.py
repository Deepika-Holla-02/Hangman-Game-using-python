import tkinter as tk
from tkinter import simpledialog  # add this at the top with other imports
from tkinter import messagebox
import random
import json
import os
import word_file
import hangman_stages

# --- Leaderboard File ---
LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_leaderboard(board):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(board, f)

leaderboard = load_leaderboard()

# --- Functions for Leaderboard ---
def show_leaderboard():
    if not leaderboard:
        messagebox.showinfo("Leaderboard", "No scores yet!")
        return

    # Sort by score (highest first)
    sorted_board = sorted(leaderboard, key=lambda x: x["score"], reverse=True)

    # Create custom leaderboard window
    lb_window = tk.Toplevel(root)
    lb_window.title("🏆 Leaderboard")
    lb_window.geometry("500x300")  # bigger size
    lb_window.config(bg="#f0f8ff")

    title = tk.Label(lb_window, text="🏆 Leaderboard 🏆", font=("Arial", 20, "bold"), bg="#4682b4", fg="white")
    title.pack(fill="x", pady=10)

    # Show top 10 players
    for i, item in enumerate(sorted_board[:10]):
        tk.Label(lb_window,text=f"{i+1}. {item.get('name','Unknown')} - {item['score']} points",font=("Arial", 14),bg="#f0f8ff",anchor="w").pack(pady=2, padx=20, anchor="w")

    close_btn = tk.Button(lb_window, text="Close", command=lb_window.destroy,font=("Arial", 12, "bold"), bg="#6a5acd", fg="white")
    close_btn.pack(pady=15)

# --- Hangman Game Window ---
def start_game():
    game_window = tk.Toplevel(root)
    game_window.title("Hangman Game")
    game_window.geometry("900x550")
    game_window.config(bg="#f0f8ff")

    # Game Setup 
    chosen_word = random.choice(word_file.words)
    lives = 6
    display = ["_"] * len(chosen_word)
    score = 0  

    def update_display():
        word_label.config(text=" ".join(display))
        hangman_label.config(text=hangman_stages.stages[lives])
        score_label.config(text=f"Score: {score}")  

    def restart_game():
        nonlocal chosen_word, lives, display, score
        chosen_word = random.choice(word_file.words)
        lives = 6
        display = ["_"] * len(chosen_word)
        score = 0  
        update_display()

    def guess_letter():
        nonlocal lives, score
        letter = entry.get().lower()
        entry.delete(0, tk.END)

        if not letter.isalpha() or len(letter) != 1:
            messagebox.showwarning("Invalid Input", "⚠️ Please enter a single alphabet.")
            return

        if letter in chosen_word:
            for i in range(len(chosen_word)):
                if chosen_word[i] == letter:
                    if display[i] == "_":  
                        display[i] = letter
                        score += 2  
        else:
            lives -= 1
            if score > 0:
                score -= 1  

        update_display()

        if "_" not in display:  # WIN
            final_score = score + 10
            # ask name after game over
            play_again = messagebox.askyesno("Game Over", f"🎉 YOU WIN!!!\nFinal Score: {final_score}\n\nDo you want to continue?")
            
            player_name = simpledialog.askstring("Player Name", "Enter your name:")
            if player_name:
                leaderboard.append({"name": player_name, "score": final_score})
                save_leaderboard(leaderboard)

            if play_again:
                restart_game()
            else:
                show_leaderboard()
                game_window.destroy()

        elif lives == 0:  # LOSE
            play_again = messagebox.askyesno("Game Over", f"💀 YOU LOSE!!!\nWord was: {chosen_word}\nFinal Score: {score}\n\nDo you want to continue?")
            
            player_name = simpledialog.askstring("Player Name", "Enter your name:")
            if player_name:
                leaderboard.append({"name": player_name, "score": score})
                save_leaderboard(leaderboard)

            if play_again:
                restart_game()
            else:
                show_leaderboard()
                game_window.destroy()


    # --- Widgets in Game Window ---
    title_label = tk.Label(game_window, text="🎯 Hangman Game 🎯", font=("Arial", 24, "bold"), fg="#ffffff", bg="#4682b4", padx=10, pady=10)
    title_label.pack(pady=10, fill="x")

    score_label = tk.Label(game_window, text=f"Score: {score}", font=("Arial", 16, "bold"), fg="#8b0000", bg="#f0f8ff")
    score_label.pack(pady=5)

    hangman_label = tk.Label(game_window, text=hangman_stages.stages[lives], font=("Courier", 14, "bold"), fg="#ff4500", bg="#f0f8ff")
    hangman_label.pack()

    word_label = tk.Label(game_window, text=" ".join(display), font=("Arial", 22, "bold"), fg="#2e8b57", bg="#f0f8ff")
    word_label.pack(pady=20)

    entry = tk.Entry(game_window, font=("Arial", 16), fg="#000080", bg="#e6e6fa", justify="center")
    entry.pack(pady=10)

    guess_button = tk.Button(game_window, text="Guess", command=guess_letter, font=("Arial", 16, "bold"), fg="white", bg="#6a5acd", activebackground="#483d8b", relief="raised", width=10)
    guess_button.pack(pady=15)

    update_display()

# --- Main Menu Window ---
root = tk.Tk()
root.title("Hangman - Main Menu")
root.geometry("500x300")
root.config(bg="#f0f8ff")

title_label = tk.Label(root, text="🎯 Hangman Game 🎯", font=("Arial", 28, "bold"), fg="#ffffff", bg="#4682b4", padx=10, pady=10)
title_label.pack(pady=20, fill="x")

start_button = tk.Button(root, text="Start Game", command=start_game, font=("Arial", 16, "bold"), fg="white", bg="#6a5acd", width=15)
start_button.pack(pady=20)

leaderboard_button = tk.Button(root, text="Show Leaderboard", command=show_leaderboard, font=("Arial", 16, "bold"), fg="white", bg="#228b22", width=15)
leaderboard_button.pack(pady=10)

root.mainloop()
