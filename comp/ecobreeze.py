from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import random

# Main app
app = tk.Tk()
app.title("EcoBreeze")
app.geometry('800x800')

name = ""
point_value = 0

# Script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Image paths
background_path = os.path.join(script_dir, "background.png")

# Load background image
background_img = Image.open(background_path)
background_pic = ImageTk.PhotoImage(background_img)

# Set background image
background_label = tk.Label(app, image=background_pic)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Username input
login_label = tk.Label(app, text="QUICK LOGIN", font=("Arial", 24))
login_label.place(x=300, y=200)

login_entry = tk.Entry(app, font=("Arial", 20))
login_entry.place(x=250, y=270)

login_button = tk.Button(app, text="START", font=("Arial", 18))
login_button.place(x=340, y=330)

# Global variables
change_random_job = None
update_table_job = None
widgets_to_hide = []

def start_game():
    global name
    name = login_entry.get().strip()

    if not name:
        login_label.config(text="Please enter your name!")
        return

    login_label.place_forget()
    login_entry.place_forget()
    login_button.place_forget()

    setup_game()

login_button.config(command=start_game)

def setup_game():
    global welcome, ecoquest_button, current_pm25_value, random_label, pm25_status_label, leaderboard_label, table
    global change_random_job, update_table_job, points_label, point_value

    # Welcome
    welcome = tk.Label(app, text=f"Welcome, {name}", font=("Arial", 24))
    welcome.place(x=340, y=50)

    # EcoQuest Button
    ecoquest_path = os.path.join(script_dir, "ecoquest.jpg")
    ecoquest_img = Image.open(ecoquest_path).resize((200, 100))
    ecoquest_pic = ImageTk.PhotoImage(ecoquest_img)

    ecoquest_button = tk.Button(app, image=ecoquest_pic, command=open_ecoquest)
    ecoquest_button.image = ecoquest_pic
    ecoquest_button.place(x=580, y=150)

    # EcoBot button
    ecobot_path = os.path.join(script_dir, "ecobot.png")
    ecobot_img = Image.open(ecobot_path).resize((200, 100))
    ecobot_pic = ImageTk.PhotoImage(ecobot_img)

    ecobot_button = tk.Button(app, image=ecobot_pic, command=ecobot)
    ecobot_button.image = ecobot_pic
    ecobot_button.place(x=10, y=150)

    # PM2.5 Display
    current_pm25_value = random.randint(0, 125)
    random_label = tk.Label(app, text=f"{current_pm25_value}μg/m3 of PM2.5", font=("Arial", 24))
    random_label.place(x=445, y=400)

    pm25_status_label = tk.Label(app, text="", font=("Gabriel Sans", 20), wraplength=500, justify="center")
    pm25_status_label.place(x=300, y=280, width=500, height=100)

    # Points display
    points_label = tk.Label(app, text=f"Points: {point_value}", font=("Arial", 24))
    points_label.place(x=590, y=10)

    def change_random_number():
        global current_pm25_value, change_random_job
        try:
            current_pm25_value = random.randint(0, 125)
            random_label.config(text=f'{current_pm25_value}μg/m3 of PM2.5')

            if current_pm25_value < 9:
                status = "Air quality is good and poses little or no risk!"
                status_color = "green"
            elif 9 <= current_pm25_value < 35:
                status = "Acceptable, but sensitive groups may feel slight effects."
                status_color = "yellow"
            elif 35 <= current_pm25_value < 55:
                status = "People with asthma, children, and old people should be cautious."
                status_color = "orange"
            elif 55 <= current_pm25_value < 80:
                status = "Everyone may begin to feel health effects."
                status_color = "#f47126"
            else:
                status = "Serious health effects, emergency conditions."
                status_color = "red"

            pm25_status_label.config(text=status, fg=status_color)

        except tk.TclError:
            return
        
        change_random_job = app.after(1500, change_random_number)

    change_random_number()

    # Leaderboard
    leaderboard_label = tk.Label(app, text="LEADERBOARD", font=("Arial", 24))
    leaderboard_label.place(x=85, y=430)

    table = ttk.Treeview(app, columns=("Position", "Name", "Score", "Status"), show="headings")
    table.heading("Position", text="Position")
    table.heading("Name", text="Name")
    table.heading("Score", text="Score")
    table.heading("Status", text="Status")

    table.column("Position", width=80)
    table.column("Name", width=150)
    table.column("Score", width=100)
    table.column("Status", width=200)

    table.place(x=5, y=500, height=280)

    bot_users = ["Charlie", "Mark", "Bob"]
    user_scores = {user: random.randint(100, 400) for user in bot_users}
    user_scores[name] = point_value

    def update_table():
        global update_table_job
        try:
            user_to_update = random.choice(bot_users)
            user_scores[user_to_update] += random.randint(1, 100)

            table.delete(*table.get_children())

            all_users = bot_users + [name]
            random.shuffle(all_users)

            sorted_users = sorted([(user, user_scores[user]) for user in all_users], key=lambda x: x[1], reverse=True)
            positions = ["1st", "2nd", "3rd"] + [f"{i+1}th" for i in range(3, len(sorted_users))]

            for idx, (user, score) in enumerate(sorted_users):
                status = "Good" if score > 400 else "Needs Improvement"
                row_id = table.insert("", "end", values=(positions[idx], user, score, status))

                if idx < 3:
                    table.tag_configure(f"green_row_{idx}", background="lightgreen")
                    table.item(row_id, tags=(f"green_row_{idx}",))

        except tk.TclError:
            return

        update_table_job = app.after(1000, update_table)

    update_table()

    widgets_to_hide.clear()
    widgets_to_hide.extend([welcome, ecoquest_button, random_label, pm25_status_label,
                           leaderboard_label, table, points_label])

def open_ecoquest():
    global change_random_job, update_table_job, level1_button, level2_button

    # Cancel timers
    if change_random_job:
        app.after_cancel(change_random_job)
    if update_table_job:
        app.after_cancel(update_table_job)

    # Hide and destroy old widgets
    for widget in widgets_to_hide:
        widget.destroy()

    # Level 1 button
    level1_path = os.path.join(script_dir, "level1.jpg")
    level1_img = Image.open(level1_path).resize((200, 100))
    level1_pic = ImageTk.PhotoImage(level1_img)

    level1_button = tk.Button(app, image=level1_pic, command=lambda: open_task1())
    level1_button.image = level1_pic
    level1_button.place(x=320, y=50)

    # Level 2 button
    level2_path = os.path.join(script_dir, "level2.png")
    level2_img = Image.open(level2_path).resize((200, 100))
    level2_pic = ImageTk.PhotoImage(level2_img)

    level2_button = tk.Button(app, image=level2_pic, command=lambda: open_task2())
    level2_button.image = level2_pic
    level2_button.place(x=320, y=200)

    # Level 4 button
    level4_path = os.path.join(script_dir, "level4.png")
    level4_img = Image.open(level4_path).resize((200, 100))
    level4_pic = ImageTk.PhotoImage(level4_img)

    level4_button = tk.Button(app, image=level4_pic, command=lambda: open_task4())
    level4_button.image = level4_pic
    level4_button.place(x=320, y=500)

    # Level 3 button
    level3_path = os.path.join(script_dir, "level3.png")
    level3_img = Image.open(level3_path).resize((200, 100))
    level3_pic = ImageTk.PhotoImage(level3_img)

    level3_button = tk.Button(app, image=level3_pic, command=lambda: open_task3())
    level3_button.image = level3_pic
    level3_button.place(x=320, y=350)

    # Level 5 button
    level5_path = os.path.join(script_dir, "level5.png")
    level5_img = Image.open(level5_path).resize((200, 100))
    level5_pic = ImageTk.PhotoImage(level5_img)

    level5_button = tk.Button(app, image=level5_pic, command=lambda: open_task5())
    level5_button.image = level5_pic
    level5_button.place(x=320, y=650)

def open_task1():
    for widget in app.place_slaves():
        widget.place_forget()

    background_label = tk.Label(app, image=background_pic)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    task_heading = tk.Label(app, text="Task 1", font=("Arial", 36))
    task_heading.place(x=350, y=10)

    task_label = tk.Label(app, text="Plant a tree!", font=("Arial", 40))
    task_label.place(x=280, y=300)

    completed_path = os.path.join(script_dir, "completed.png")
    completed_img = Image.open(completed_path).resize((200, 100))
    completed_pic = ImageTk.PhotoImage(completed_img)

    completed_button = tk.Button(app, image=completed_pic, command=lambda: task_completed1(task_heading, task_label, completed_button))
    completed_button.image = completed_pic
    completed_button.place(x=320, y=600)

def open_task2():
    for widget in app.place_slaves():
        widget.place_forget()
    
    background_label = tk.Label(app, image=background_pic)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    task_heading = tk.Label(app, text="Task 2", font=("Arial", 36))
    task_heading.place(x=350, y=10)

    task_label = tk.Label(app, text="Listen to calm music!", font=("Arial", 40))
    task_label.place(x=160, y=300)

    completed_path = os.path.join(script_dir, "completed.png")
    completed_img = Image.open(completed_path).resize((200, 100))
    completed_pic = ImageTk.PhotoImage(completed_img)

    completed_button = tk.Button(app, image=completed_pic, command=lambda: task_completed2(task_heading, task_label, completed_button))
    completed_button.image = completed_pic
    completed_button.place(x=320, y=600)

def open_task3():
    for widget in app.place_slaves():
        widget.place_forget()

    background_label = tk.Label(app, image=background_pic)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    task_heading = tk.Label(app, text="Task 3", font=("Arial", 36))
    task_heading.place(x=350, y=10)

    task_label = tk.Label(app, text="Turn off the lights!", font=("Arial", 40))
    task_label.place(x=200, y=300)

    completed_path = os.path.join(script_dir, "completed.png")
    completed_img = Image.open(completed_path).resize((200, 100))
    completed_pic = ImageTk.PhotoImage(completed_img)

    completed_button = tk.Button(app, image=completed_pic, command=lambda: task_completed3(task_heading, task_label, completed_button))
    completed_button.image = completed_pic
    completed_button.place(x=320, y=600)

def open_task4():
    for widget in app.place_slaves():
        widget.place_forget()

    background_label = tk.Label(app, image=background_pic)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    task_heading = tk.Label(app, text="Task 4", font=("Arial", 36))
    task_heading.place(x=350, y=10)

    task_label = tk.Label(app, text="Go for a walk!", font=("Arial", 40))
    task_label.place(x=240, y=300)

    completed_path = os.path.join(script_dir, "completed.png")
    completed_img = Image.open(completed_path).resize((200, 100))
    completed_pic = ImageTk.PhotoImage(completed_img)

    completed_button = tk.Button(app, image=completed_pic, command=lambda: task_completed4(task_heading, task_label, completed_button))
    completed_button.image = completed_pic
    completed_button.place(x=320, y=550)

def open_task5():
    for widget in app.place_slaves():
        widget.place_forget()

    background_label = tk.Label(app, image=background_pic)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    task_heading = tk.Label(app, text="Task 5", font=("Arial", 36))
    task_heading.place(x=350, y=10)

    task_label = tk.Label(app, text="Do some exercise!", font=("Arial", 40))
    task_label.place(x=200, y=300)

    completed_path = os.path.join(script_dir, "completed.png")
    completed_img = Image.open(completed_path).resize((200, 100))
    completed_pic = ImageTk.PhotoImage(completed_img)

    completed_button = tk.Button(app, image=completed_pic, command=lambda: task_completed5(task_heading, task_label, completed_button))
    completed_button.image = completed_pic
    completed_button.place(x=300, y=650)

def task_completed1(task_heading, task_label, completed_button):
    global point_value
    task_heading.place_forget()
    task_label.place_forget()
    completed_button.place_forget()

    tick_path = os.path.join(script_dir, "completed_tick.png")
    tick_img = Image.open(tick_path).resize((200, 100))
    tick_pic = ImageTk.PhotoImage(tick_img)

    tick_label = tk.Label(app, image=tick_pic)
    tick_label.image = tick_pic
    tick_label.place(x=320, y=600)

    point_value += random.randint(40, 100)

    back_path = os.path.join(script_dir, "back.png")
    back_img = Image.open(back_path).resize((200, 100))
    back_pic = ImageTk.PhotoImage(back_img)

    def go_back():
        tick_label.place_forget()
        back_button.place_forget()
        setup_game()

    back_button = tk.Button(app, image=back_pic, command=go_back)
    back_button.image = back_pic
    back_button.place(x=5, y=5)

def task_completed2(task_heading, task_label, completed_button):
    global point_value
    task_heading.place_forget()
    task_label.place_forget()
    completed_button.place_forget()

    tick_path = os.path.join(script_dir, "completed_tick.png")
    tick_img = Image.open(tick_path).resize((200, 100))
    tick_pic = ImageTk.PhotoImage(tick_img)

    tick_label = tk.Label(app, image=tick_pic)
    tick_label.image = tick_pic
    tick_label.place(x=320, y=600)

    point_value += random.randint(1, 20)

    back_path = os.path.join(script_dir, "back.png")
    back_img = Image.open(back_path).resize((200, 100))
    back_pic = ImageTk.PhotoImage(back_img)

    def go_back():
        tick_label.place_forget()
        back_button.place_forget()
        setup_game()

    back_button = tk.Button(app, image=back_pic, command=go_back)
    back_button.image = back_pic
    back_button.place(x=5, y=5)

def task_completed3(task_heading, task_label, completed_button):
    global point_value
    task_heading.place_forget()
    task_label.place_forget()
    completed_button.place_forget()

    tick_path = os.path.join(script_dir, "completed_tick.png")
    tick_img = Image.open(tick_path).resize((200, 100))
    tick_pic = ImageTk.PhotoImage(tick_img)

    tick_label = tk.Label(app, image=tick_pic)
    tick_label.image = tick_pic
    tick_label.place(x=320, y=600)

    point_value += random.randint(1, 10)

    back_path = os.path.join(script_dir, "back.png")
    back_img = Image.open(back_path).resize((200, 100))
    back_pic = ImageTk.PhotoImage(back_img)

    def go_back():
        tick_label.place_forget()
        back_button.place_forget()
        setup_game()

    back_button = tk.Button(app, image=back_pic, command=go_back)
    back_button.image = back_pic
    back_button.place(x=5, y=5)

def task_completed4(task_heading, task_label, completed_button):
    global point_value
    task_heading.place_forget()
    task_label.place_forget()
    completed_button.place_forget()

    tick_path = os.path.join(script_dir, "completed_tick.png")
    tick_img = Image.open(tick_path).resize((200, 100))
    tick_pic = ImageTk.PhotoImage(tick_img)

    tick_label = tk.Label(app, image=tick_pic)
    tick_label.image = tick_pic
    tick_label.place(x=320, y=600)

    point_value += random.randint(100, 200)

    back_path = os.path.join(script_dir, "back.png")
    back_img = Image.open(back_path).resize((200, 100))
    back_pic = ImageTk.PhotoImage(back_img)

    def go_back():
        tick_label.place_forget()
        back_button.place_forget()
        setup_game()

    back_button = tk.Button(app, image=back_pic, command=go_back)
    back_button.image = back_pic
    back_button.place(x=5, y=5)

def task_completed5(task_heading, task_label, completed_button):
    global point_value, tick_label
    task_heading.place_forget()
    task_label.place_forget()
    completed_button.place_forget()

    tick_path = os.path.join(script_dir, "completed_tick.png")
    tick_img = Image.open(tick_path).resize((200, 100))
    tick_pic = ImageTk.PhotoImage(tick_img)

    tick_label = tk.Label(app, image=tick_pic)
    tick_label.image = tick_pic
    tick_label.place(x=320, y=600)

    point_value += random.randint(100, 200)

    back_path = os.path.join(script_dir, "back.png")
    back_img = Image.open(back_path).resize((200, 100))
    back_pic = ImageTk.PhotoImage(back_img)

    def go_back():
        tick_label.place_forget()
        back_button.place_forget()
        setup_game()

    back_button = tk.Button(app, image=back_pic, command=go_back)
    back_button.image = back_pic
    back_button.place(x=5, y=5)

# EcoBot function
chat_sequence = [
    ("EcoChat", "Hello there! How are you feeling today?"),
    {
        "I'm okay 😊": ("EcoChat", "That's good to hear! Remember to take deep breaths 🌬️"),
        "Feeling a bit stressed 😞": ("EcoChat", "That's completely okay. I'm here for you. Want a breathing exercise or a fun quote?"),
        "Not sure... 🤔": ("EcoChat", "That's totally valid. Let's figure it out together 🌟")
    },
    {
        "Breathing exercise 🧘": ("EcoChat", "Inhale... 1... 2... 3... Exhale... 1... 2... 3... Feel better?"),
        "Fun quote ✨": ("EcoChat", "“You don't have to control your thoughts. You just have to stop letting them control you.” - Dan Millman"),
        "Let's chat more 💬": ("EcoChat", "Sure! What would you like to talk about?")
    },
    {
        "I like nature 🍃": ("EcoChat", "Nature is a great healer! Even looking at trees can lower stress levels."),
        "Tell me a joke 😄": ("EcoChat", "Why don’t skeletons fight each other? They don’t have the guts."),
        "Motivation quote 💡": ("EcoChat", "“Believe you can and you're halfway there.” – Theodore Roosevelt")
    },
    {
        "Any advice? 🧠": ("EcoChat", "It’s okay to pause. Resting isn’t quitting."),
        "Can I vent? 😥": ("EcoChat", "Of course. I'm listening. Just breathe and type it out."),
        "Just distract me 🎲": ("EcoChat", "Think of your favorite food. Imagine you’re eating it now. 😋")
    },
    {
        "Thanks 💖": ("EcoChat", "You're welcome! Always here when you need me 🌈"),
        "Goodbye 👋": ("EcoChat", "Take care! You matter 💫"),
    }
]

def ecobot():
    for widget in app.place_slaves():
        widget.place_forget()

    back_path = os.path.join(script_dir, "back.png")
    back_img = Image.open(back_path).resize((200, 100))
    back_pic = ImageTk.PhotoImage(back_img)

    background_label = tk.Label(app, image=background_pic)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def go_back():
        back_button.place_forget()
        for widget in app.place_slaves():
            widget.place_forget()
        background_label = tk.Label(app, image=background_pic)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        setup_game()

    back_button = tk.Button(app, image=back_pic, command=go_back)
    back_button.image = back_pic
    back_button.place(x=5, y=5)

    # Step 2: Create chat display
    chat_frame = tk.Frame(app, bg="#ffffff", bd=2, relief="sunken")
    chat_frame.place(x=20, y=20, width=560, height=280)

    chat_log = tk.Text(chat_frame, bg="#fefefe", fg="#333", font=("Arial", 12), wrap="word")
    chat_log.pack(fill="both", expand=True)
    chat_log.config(state='disabled')

    # Step 3: Button response frame
    response_frame = tk.Frame(app, bg="#e0f7fa")
    response_frame.place(x=20, y=310, width=560, height=90)

    # Step 4: Chat sequence control
    global current_step
    current_step = 0

    def display_message(sender, message):
        chat_log.config(state='normal')
        chat_log.insert("end", f"{sender}: {message}\n")
        chat_log.config(state='disabled')
        chat_log.yview("end")

    def clear_buttons():
        for widget in response_frame.winfo_children():
            widget.destroy()

    def show_next_options():
        global current_step
        if current_step >= len(chat_sequence):
            display_message("EcoChat", "I'm always here if you want to talk again 🌈")
            clear_buttons()
            return

        step = chat_sequence[current_step]

        if isinstance(step, tuple):
            sender, message = step
            display_message(sender, message)
            current_step += 1
            show_next_options()

        elif isinstance(step, dict):
            clear_buttons()
            for reply, response in step.items():
                btn = tk.Button(response_frame, text=reply, font=("Arial", 10),
                                command=lambda r=reply: on_user_reply(r))
                btn.pack(side="top", pady=3, fill="x", padx=8)

    def on_user_reply(reply):
        global current_step
        display_message("You", reply)
        response = chat_sequence[current_step][reply]
        current_step += 1
        display_message(*response)
        current_step += 1
        show_next_options()

    # Start conversation
    show_next_options()
# Start app
app.mainloop()
