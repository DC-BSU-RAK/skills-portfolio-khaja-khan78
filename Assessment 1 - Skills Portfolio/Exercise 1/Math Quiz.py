import tkinter as tk
from tkinter import messagebox
import random

# ================= Helper Functions ================= #

def randomInt(level):
    return random.randint(1, 9) if level == "easy" else random.randint(10, 99) if level == "moderate" else random.randint(1000, 9999)

def decideOperation():
    return random.choice(["+", "-"])

def darker_color(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(max(int(int(hex_color[i:i + 2], 16) * 0.85), 0) for i in (0, 2, 4))
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def draw_rounded_bar(canvas, x, y, bar_width, height, fill, tag=None):
    """Draw rounded progress/timer bar without outlines."""
    r = height // 2
    parts = []
    parts.append(canvas.create_oval(x, y, x + height, y + height,
                                    fill=fill, outline="", tag=tag))
    parts.append(canvas.create_oval(x + bar_width - height, y, x + bar_width, y + height,
                                    fill=fill, outline="", tag=tag))
    parts.append(canvas.create_rectangle(x + r, y, x + bar_width - r, y + height,
                                         fill=fill, outline="", tag=tag))
    return parts

# ================= Core Game Logic ================= #

def displayMenu():
    clear_overlay()
    overlay.config(bg="#ffffff")
    tk.Label(overlay, text="Select Difficulty Level", font=("Helvetica", 18, "bold"), bg="#ffffff").pack(pady=20)
    for level, text in [("easy", "Easy (1-digit)"), ("moderate", "Moderate (2-digit)"), ("advanced", "Advanced (4-digit)")]:
        btn = tk.Button(overlay, text=text, width=20, font=("Helvetica", 14, "bold"),
                        bg="#4caf50", fg="white", activebackground="#45a049",
                        command=lambda l=level: start_quiz(l))
        btn.pack(pady=8)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#45a049"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#4caf50"))

def displayProblem():
    global num1, num2, operation, answer_entry, attempt, timer, timer_canvas, timer_bar_parts, timer_job

    clear_overlay()

    operation = decideOperation()
    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    attempt = 1
    if operation == "-" and num1 < num2:
        num1, num2 = num2, num1

    tk.Label(overlay, text=f"Question {question_number}/10", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(pady=(10, 5))

    # Grey progress bar (top)
    progress_canvas = tk.Canvas(overlay, width=300, height=20, bg="#ffffff", highlightthickness=0)
    progress_canvas.pack(pady=(0, 15))
    draw_rounded_bar(progress_canvas, 0, 0, 300, 20, fill="#eeeeee")
    progress_width = int((question_number - 1) / 10 * 300)
    draw_rounded_bar(progress_canvas, 0, 0, progress_width, 20, fill="#9e9e9e")

    # Problem text
    tk.Label(overlay, text=f"{num1} {operation} {num2} =", font=("Helvetica", 30, "bold"), bg="#ffffff", fg="#333333").pack(pady=10)

    # Answer entry
    answer_entry = tk.Entry(overlay, font=("Helvetica", 16), justify="center", bd=2, relief="groove")
    answer_entry.pack(pady=10)
    answer_entry.focus()

    # Submit + menu buttons
    submit_btn = tk.Button(
        overlay, text="Submit Answer", font=("Helvetica", 14, "bold"),
        bg="#2196f3", fg="white", activebackground="#1976d2", command=check_answer
    )
    submit_btn.pack(pady=10)

    menu_btn = tk.Button(overlay, text="Back to Menu", font=("Helvetica", 12),
                         bg="#ff9800", fg="white", command=displayMenu)
    menu_btn.pack(pady=5)

    # Timer
    timer_canvas = tk.Canvas(overlay, width=300, height=30, bg="#ffffff", highlightthickness=0)
    timer_canvas.pack(pady=15)
    draw_rounded_bar(timer_canvas, 0, 0, 300, 30, fill="#dddddd")
    timer_bar_parts = draw_rounded_bar(timer_canvas, 0, 0, 300, 30, fill="#4caf50", tag="bar")
    timer_canvas.create_text(150, 15, text="60s", fill="black", font=("Helvetica", 12, "bold"), tag="timer_text")

    global timer
    timer = 60
    countdown_bar()

def countdown_bar():
    global timer, timer_job
    if timer > 0:
        red = int(255 * (1 - timer / 60))
        green = int(255 * (timer / 60))
        color = f'#{red:02x}{green:02x}00'

        width = int(300 * (timer / 60))
        timer_canvas.delete("bar")
        draw_rounded_bar(timer_canvas, 0, 0, width, 30, fill=color, tag="bar")
        timer_canvas.itemconfig("timer_text", text=f"{int(timer)}s")

        timer -= 0.1
        timer_job = overlay.after(100, countdown_bar)
    else:
        timer_canvas.delete("bar")
        draw_rounded_bar(timer_canvas, 0, 0, 0, 30, fill="#ff0000", tag="bar")
        timer_canvas.itemconfig("timer_text", text="0s")
        messagebox.showinfo("Time's Up!", "⏰ Time is up! Moving to next question.")
        next_question()

def isCorrect(user_answer):
    return user_answer == (num1 + num2 if operation == "+" else num1 - num2)

def check_answer():
    global score, question_number, attempt, timer
    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a number.")
        return

    if isCorrect(user_answer):
        points = 10 if attempt == 1 else 5
        score += points
        messagebox.showinfo("Correct!", f"✅ Correct! +{points} points")
        timer = 0
        next_question()
    else:
        if attempt == 1:
            attempt += 1
            messagebox.showinfo("Incorrect", "❌ Wrong! Try again.")
        else:
            messagebox.showinfo("Incorrect", "❌ Wrong again! Moving to next question.")
            timer = 0
            next_question()

def next_question():
    global question_number, timer
    question_number += 1
    timer = 60
    if question_number > 10:
        displayResults()
    else:
        displayProblem()

def displayResults():
    clear_overlay()
    overlay.config(bg="#ffffff")
    rank = "A+" if score >= 90 else "A" if score >= 80 else "B" if score >= 70 else "C" if score >= 60 else "Needs Improvement"
    tk.Label(overlay, text="Quiz Complete!", font=("Helvetica", 22, "bold"), bg="#ffffff", fg="#333333").pack(pady=20)
    tk.Label(overlay, text=f"Final Score: {score}/100", font=("Helvetica", 16), bg="#ffffff").pack(pady=10)
    tk.Label(overlay, text=f"Rank: {rank}", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#4caf50").pack(pady=10)
    for text, cmd, color in [("Play Again", displayMenu, "#4caf50"), ("Exit", root.quit, "#f44336")]:
        btn = tk.Button(overlay, text=text, font=("Helvetica", 14, "bold"), bg=color, fg="white", command=cmd, width=15)
        btn.pack(pady=8)
        btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=darker_color(c)))
        btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))

def start_quiz(level):
    global difficulty, score, question_number
    difficulty = level
    score = 0
    question_number = 1
    displayProblem()

def clear_overlay():
    for widget in overlay.winfo_children():
        widget.destroy()

# ================= Gradient Background ================= #

def draw_gradient(canvas, color1, color2):
    """Draw a smooth vertical gradient."""
    for i in range(550):
        r1, g1, b1 = canvas.winfo_rgb(color1)
        r2, g2, b2 = canvas.winfo_rgb(color2)
        r = int(r1 + (r2 - r1) * i / 550) >> 8
        g = int(g1 + (g2 - g1) * i / 550) >> 8
        b = int(b1 + (b2 - b1) * i / 550) >> 8
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, 500, i, fill=color)

# ================= Intro Screen ================= #

def show_intro():
    clear_overlay()
    overlay.config(bg="#ffffff")
    tk.Label(overlay, text="🎓 Welcome to the Maths Quiz!", font=("Helvetica", 22, "bold"), bg="#ffffff").pack(pady=40)
    tk.Label(overlay, text="Test your brain, beat the timer,\nand earn the highest rank!", font=("Helvetica", 14), bg="#ffffff").pack(pady=10)
    root.after(3000, show_start_screen)  # show menu after 3 seconds

def show_start_screen():
    clear_overlay()
    tk.Label(overlay, text="📑💭Maths Quiz !?🤓🤔", font=("Helvetica", 26, "bold"), bg="#FFFFFF", fg="#000000").pack(pady=20)
    start_btn = tk.Button(overlay, text="Start Quiz", font=("Helvetica", 16, "bold"), bg="#2196f3", fg="white", width=20, command=displayMenu)
    start_btn.pack(pady=10)
    exit_btn = tk.Button(overlay, text="Exit", font=("Helvetica", 16, "bold"), bg="#f44336", fg="white", width=20, command=root.quit)
    exit_btn.pack(pady=5)

# ================= Main Window ================= #

root = tk.Tk()
root.title("Maths Quiz")
root.geometry("500x550")
root.resizable(False, False)

bg_canvas = tk.Canvas(root, width=500, height=550, highlightthickness=0)
bg_canvas.pack(fill="both", expand=True)
draw_gradient(bg_canvas, "#89f7fe", "#66a6ff")

overlay = tk.Frame(root, bg="#ffffff", bd=3, relief="ridge", highlightbackground="#bbbbbb", highlightthickness=2)
overlay.place(relx=0.5, rely=0.5, anchor="center")

show_intro()

root.mainloop()
