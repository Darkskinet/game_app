import streamlit as st
import random
from PIL import Image
import os

# Script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load background image
background_path = os.path.join(script_dir, "background.png")
background_img = Image.open(background_path)

# Initialize global variables
name = ""
point_value = 0
user_scores = {}
bot_users = ["Charlie", "Mark", "Bob"]

def welcome_screen():
    global name
    st.image(background_img, use_column_width=True)
    st.title("EcoBreeze")
    name = st.text_input("QUICK LOGIN", "")
    
    if st.button("START"):
        if not name.strip():
            st.error("Please enter your name!")
        else:
            st.session_state['name'] = name
            setup_game()

def setup_game():
    global point_value
    point_value = 0
    st.title(f"Welcome, {st.session_state['name']}")
    
    # EcoQuest Button
    if st.button("Open EcoQuest"):
        open_ecoquest()

    # PM2.5 Display
    current_pm25_value = random.randint(0, 125)
    st.write(f"{current_pm25_value} μg/m3 of PM2.5")
    display_pm25_status(current_pm25_value)

    # Points display
    st.write(f"Points: {point_value}")

    # Leaderboard
    if 'user_scores' not in st.session_state:
        st.session_state['user_scores'] = {user: random.randint(100, 400) for user in bot_users}
        st.session_state['user_scores'][st.session_state['name']] = point_value
    update_leaderboard()

def display_pm25_status(value):
    if value < 9:
        st.success("Air quality is good and poses little or no risk!")
    elif 9 <= value < 35:
        st.warning("Acceptable, but sensitive groups may feel slight effects.")
    elif 35 <= value < 55:
        st.warning("People with asthma, children, and old people should be cautious.")
    elif 55 <= value < 80:
        st.error("Everyone may begin to feel health effects.")
    else:
        st.error("Serious health effects, emergency conditions.")

def update_leaderboard():
    st.subheader("LEADERBOARD")
    all_users = list(st.session_state['user_scores'].keys())
    sorted_users = sorted(all_users, key=lambda x: st.session_state['user_scores'][x], reverse=True)
    leaderboard_data = [(idx + 1, user, st.session_state['user_scores'][user]) for idx, user in enumerate(sorted_users)]
    for position, user, score in leaderboard_data:
        st.write(f"{position}. {user} - {score} points")

def open_ecoquest():
    st.subheader("Choose a Task:")
    tasks = {
        "Task 1: Plant a tree!": (40, "Task 1"),
        "Task 2: Listen to calm music!": (1, "Task 2"),
        "Task 3: Turn off the lights!": (1, "Task 3"),
        "Task 4: Go for a walk!": (100, "Task 4"),
        "Task 5: Do some exercise!": (100, "Task 5")
    }
    selected_task = st.selectbox("Select a task", list(tasks.keys()))
    
    if st.button("Complete Task"):
        complete_task(selected_task, tasks[selected_task][0])

def complete_task(task, points):
    global point_value
    point_value += random.randint(points, points + 60)  # Random points based on the task
    st.success(f"You completed: {task}! You earned points!")
    st.session_state['user_scores'][st.session_state['name']] = point_value
    update_leaderboard()

def main():
    if 'name' not in st.session_state:
        welcome_screen()
    else:
        setup_game()

if __name__ == "__main__":
    main()
