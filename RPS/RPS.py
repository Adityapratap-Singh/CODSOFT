import tkinter as tk
import random
from tkinter import messagebox

# Choices
choices = ['Rock', 'Paper', 'Scissors']

# Initialize scores
user_score = 0
computer_score = 0
game_over = False

# Game logic
def determine_winner(user_choice):
    global user_score, computer_score, game_over

    if game_over:
        return

    computer_choice = random.choice(choices)
    result = ""

    if user_choice == computer_choice:
        result = "It's a Tie!"
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Scissors" and computer_choice == "Paper") or \
         (user_choice == "Paper" and computer_choice == "Rock"):
        result = "You Win!"
        user_score += 1
    else:
        result = "Computer Wins!"
        computer_score += 1

    result_text.set(f"You chose: {user_choice}\nComputer chose: {computer_choice}\n\n{result}")
    score_text.set(f"Your Score: {user_score}  |  Computer Score: {computer_score}")

    if user_score == 10 or computer_score == 10:
        game_over = True
        winner = "You" if user_score == 10 else "Computer"
        messagebox.showinfo("Game Over", f"{winner} won the game!\nFinal Score:\nYou: {user_score}  |  Computer: {computer_score}")
        disable_buttons()

def reset_game():
    global user_score, computer_score, game_over
    user_score = 0
    computer_score = 0
    game_over = False
    result_text.set("Make your move!")
    score_text.set("Your Score: 0  |  Computer Score: 0")
    enable_buttons()

# Disable/Enable buttons
def disable_buttons():
    rock_btn.config(state="disabled")
    paper_btn.config(state="disabled")
    scissors_btn.config(state="disabled")

def enable_buttons():
    rock_btn.config(state="normal")
    paper_btn.config(state="normal")
    scissors_btn.config(state="normal")

# GUI setup
root = tk.Tk()
root.title("Rock-Paper-Scissors Game")
root.geometry("400x400")
root.config(bg="#f2f2f2")

# Result display
result_text = tk.StringVar()
result_text.set("Make your move!")

score_text = tk.StringVar()
score_text.set("Your Score: 0  |  Computer Score: 0")

# Title
tk.Label(root, text="Rock-Paper-Scissors", font=("Arial", 20, "bold"), bg="#f2f2f2").pack(pady=10)
tk.Label(root, textvariable=result_text, font=("Arial", 14), bg="#f2f2f2", fg="#333").pack(pady=10)
tk.Label(root, textvariable=score_text, font=("Arial", 12), bg="#f2f2f2", fg="#555").pack()

# Buttons
btn_frame = tk.Frame(root, bg="#f2f2f2")
btn_frame.pack(pady=20)

rock_btn = tk.Button(btn_frame, text="Rock", width=10, font=("Arial", 12), bg="#d9d9d9", command=lambda: determine_winner("Rock"))
rock_btn.grid(row=0, column=0, padx=10)

paper_btn = tk.Button(btn_frame, text="Paper", width=10, font=("Arial", 12), bg="#d9d9d9", command=lambda: determine_winner("Paper"))
paper_btn.grid(row=0, column=1, padx=10)

scissors_btn = tk.Button(btn_frame, text="Scissors", width=10, font=("Arial", 12), bg="#d9d9d9", command=lambda: determine_winner("Scissors"))
scissors_btn.grid(row=0, column=2, padx=10)

# Reset Button
tk.Button(root, text="Reset Game", font=("Arial", 12), bg="#ffcccc", command=reset_game).pack(pady=20)

# Exit Option
tk.Button(root, text="Exit", font=("Arial", 12), bg="#ff9999", command=root.quit).pack()

root.mainloop()
