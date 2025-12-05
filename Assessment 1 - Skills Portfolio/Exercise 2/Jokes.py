import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

class PrettyButton(tk.Canvas):
    def __init__(self, parent, text, command=None, bg_color="#4CAF50", hover_color="#45a049", text_color="white", width=150, height=40):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=parent["bg"])

        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.width = width
        self.height = height


        self.rounded_rect = self.create_rounded_rect(0, 0, width, height, 20, fill=bg_color, outline="")

    
        self.text_item = self.create_text(
            width // 2,
            height // 2,
            text=text,
            fill=text_color,
            font=("Arial", 13, "bold")
        )

 
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_click(self, event):
        if self.command:
            self.command()

    def on_enter(self, event):
        self.itemconfig(self.rounded_rect, fill=self.hover_color)

    def on_leave(self, event):
        self.itemconfig(self.rounded_rect, fill=self.bg_color)

    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2 - radius,
            x1, y1 + radius
        ]
        return self.create_polygon(points, smooth=True, **kwargs)



class JokeMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joke Machine")
        self.root.geometry("650x380")

    
        self.load_background()

   
        self.jokes = self.load_jokes()
        self.current = None

     
        self.build_start_screen()

    def load_background(self):
        try:
            bg_path = os.path.join(os.path.dirname(__file__), "background.jpg")

            img = Image.open(bg_path)
            img = img.resize((650, 380))
            self.bg_img = ImageTk.PhotoImage(img)

            self.bg_label = tk.Label(self.root, image=self.bg_img)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        except:
            messagebox.showerror("Error", "background.jpg not found!")

    def build_start_screen(self):
        self.start_frame = tk.Frame(self.root, bg="white")
        self.start_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(
            self.start_frame,
            text="Welcome to Alexa Joke Machine!",
            font=("Arial", 20, "bold"),
            bg="white"
        )
        title.pack(pady=15)

        start_btn = PrettyButton(
            self.start_frame,
            text="Start",
            bg_color="#3498db",
            hover_color="#2980b9",
            width=160,
            height=45,
            command=self.open_joke_screen
        )
        start_btn.pack(pady=10)

    def open_joke_screen(self):
        self.start_frame.destroy()

        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(pady=20)

        self.setup_label = tk.Label(
            main_frame,
            text="Click 'New Joke' to begin!",
            wraplength=550,
            font=("Arial", 15),
            bg="white"
        )
        self.setup_label.pack(pady=10)

        self.punch_label = tk.Label(
            main_frame,
            text="",
            wraplength=550,
            font=("Arial", 14, "bold"),
            fg="#006400",
            bg="white"
        )
        self.punch_label.pack(pady=10)

        btn_frame = tk.Frame(main_frame, bg="white")
        btn_frame.pack(pady=10)

     
        self.new_joke_btn = PrettyButton(
            btn_frame,
            text="New Joke",
            bg_color="#1abc9c",
            hover_color="#16a085",
            width=150,
            height=40,
            command=self.new_joke
        )
        self.new_joke_btn.grid(row=0, column=0, padx=7)

       
        self.show_btn = PrettyButton(
            btn_frame,
            text="Show Punchline",
            bg_color="#f1c40f",
            hover_color="#d4ac0d",
            width=150,
            height=40,
            command=self.show_punchline
        )
        self.show_btn.grid(row=0, column=1, padx=7)

      
        quit_btn = PrettyButton(
            main_frame,
            text="Quit",
            bg_color="#e74c3c",
            hover_color="#c0392b",
            width=150,
            height=40,
            command=self.root.quit
        )
        quit_btn.pack(pady=10)

    def load_jokes(self):
        try:
            file_path = os.path.join(os.path.dirname(__file__), "randomJokes.txt")

            jokes = []
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "?" in line:
                        setup, punch = line.split("?", 1)
                        jokes.append((setup + "?", punch.strip()))
            return jokes

        except:
            messagebox.showerror("Error", "randomJokes.txt not found!")
            return []

    def new_joke(self):
        if not self.jokes:
            self.setup_label.config(text="No jokes found.")
            return

        self.current = random.choice(self.jokes)
        self.setup_label.config(text=self.current[0])
        self.punch_label.config(text="")

    def show_punchline(self):
        if self.current:
            self.punch_label.config(text=self.current[1])



if __name__ == "__main__":
    root = tk.Tk()
    app = JokeMachineApp(root)
    root.mainloop()
