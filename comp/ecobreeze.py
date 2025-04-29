import streamlit as st
import random
from PIL import Image
import os

# Global variables
name = ""
point_value = 0
current_pm25_value = random.randint(0, 125)

# Script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load images
background_path = os.path.join(script_dir, "background.png")
ecoquest_path = os.path.join(script_dir, "ecoquest.jpg")
ecobot_path = os.path.join(script_dir, "ecobot.png")
completed_path = os.path.join(script_dir, "completed.png")
tick_path = os.path.join(script_dir, "completed_tick.png")
back_path = os.path.join(script_dir, "back.png")

# Load images
background_img = Image.open(background_path)
ecoquest_img = Image.open(ecoquest_path).resize((200, 100))
ecobot_img = Image.open(ecobot_path).resize((200, 100))
completed_img = Image.open(completed_path).resize((200, 100))
tick_img = Image.open(tick_path).resize((200, 100))
back_img = Image.open(back_path).resize((200, 100))

# Streamlit app
st.set_page_config(page_title="EcoBreeze", layout="wide")

# Background
st.image(background_img, use_column_width=True)

# Login Section
st.title("QUICK LOGIN")
name = st.text_input("Enter your name:", "")
if st.button("START"):
    if name.strip() == "":
        st.error("Please enter your name!")
    else:
        st.success(f"Welcome, {name}")
        setup_game()

def setup_game():
    global point_value, current_pm25_value

    # EcoQuest and EcoBot Buttons
    col1, col2 = st.columns(2)
    with col1:
        st.image(ecobot_img, caption="EcoBot", use_column_width=True)
    with col2:
        st.image(ecoquest_img, caption="EcoQuest", use_column_width=True)

    # PM2.5 Display
    st.write(f"{current_pm25_value}μg/m3 of PM2.5")
    update_pm25_status(current_pm25_value)

    # Points display
    st.write(f"Points: {point_value}")

    # Task Buttons
    if st.button("Task 1: Plant a tree!"):
        task_completed(1)

    if st.button("Task 2: Listen to calm music!"):
        task_completed(2)

    if st.button("Task 3: Turn off the lights!"):
        task_completed(3)

    if st.button("Task 4: Go for a walk!"):
        task_completed(4)

    if st.button("Task 5: Do some exercise!"):
        task_completed(5)

def update_pm25_status(value):
    if value < 9:
        status = "Air quality is good and poses little or no risk!"
        status_color = "green"
    elif 9 <= value < 35:
        status = "Acceptable, but sensitive groups may feel slight effects."
        status_color = "yellow"
    elif 35 <= value < 55:
        status = "People with asthma, children, and old people should be cautious."
        status_color = "orange"
    elif 55 <= value < 80:
        status = "Everyone may begin to feel health effects."
        status_color = "#f47126"
    else:
        status = "Serious health effects, emergency conditions."
        status_color = "red"
    
    st.markdown(f"<span style='color:{status_color};'>{status}</span>", unsafe_allow_html=True)

def task_completed(task_number):
    global point_value
    if task_number == 1:
        point_value += random.randint(40, 100)
    elif task_number == 2:
        point_value += random.randint(1, 20)
    elif task_number == 3:
        point_value += random.randint(1, 10)
    elif task_number == 4:
        point_value += random.randint(100, 200)
    elif task_number == 5:
        point_value += random.randint(100, 200)

    st.image(tick_img, caption="Task Completed!", use_column_width=True)
    st.write(f"Points: {point_value}")

# Run the app
if __name__ == "__main__":
    st.run()
