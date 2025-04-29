import streamlit as st
from PIL import Image
import os
import random
import pandas as pd
import time

# --- PATHS ---
script_dir = os.path.dirname(os.path.abspath(__file__))
background_path = os.path.join(script_dir, "background.png")
ecoquest_path = os.path.join(script_dir, "ecoquest.jpg")
ecobot_path = os.path.join(script_dir, "ecobot.png")
level1_path = os.path.join(script_dir, "level1.jpg")
level2_path = os.path.join(script_dir, "level2.png")
level3_path = os.path.join(script_dir, "level3.png")
level4_path = os.path.join(script_dir, "level4.png")
level5_path = os.path.join(script_dir, "level5.png")
completed_path = os.path.join(script_dir, "completed.png")
completed_tick_path = os.path.join(script_dir, "completed_tick.png")
back_path = os.path.join(script_dir, "back.png")

# --- GLOBAL VARIABLES ---
if 'name' not in st.session_state:
    st.session_state['name'] = ""
if 'point_value' not in st.session_state:
    st.session_state['point_value'] = 0
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'login'
if 'pm25_value' not in st.session_state:
    st.session_state['pm25_value'] = random.randint(0, 125)
if 'leaderboard_data' not in st.session_state:
    st.session_state['leaderboard_data'] = pd.DataFrame({
        'Position': [],
        'Name': [],
        'Score': [],
        'Status': []
    })
if 'bot_users' not in st.session_state:
    st.session_state['bot_users'] = ["Charlie", "Mark", "Bob"]
if 'user_scores' not in st.session_state:
    st.session_state['user_scores'] = {user: random.randint(100, 400) for user in st.session_state['bot_users']}
    st.session_state['user_scores'][st.session_state['name']] = st.session_state['point_value']
if 'chat_sequence_index' not in st.session_state:
    st.session_state['chat_sequence_index'] = 0
if 'chat_log' not in st.session_state:
    st.session_state['chat_log'] = []

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

# --- FUNCTIONS ---
def update_pm25():
    st.session_state['pm25_value'] = random.randint(0, 125)
    time.sleep(1.5)
    st.rerun()

def get_pm25_status(value):
    if value < 9:
        return "Air quality is good and poses little or no risk!", "green"
    elif 9 <= value < 35:
        return "Acceptable, but sensitive groups may feel slight effects.", "yellow"
    elif 35 <= value < 55:
        return "People with asthma, children, and old people should be cautious.", "orange"
    elif 55 <= value < 80:
        return "Everyone may begin to feel health effects.", "#f47126"
    else:
        return "Serious health effects, emergency conditions.", "red"

def update_leaderboard():
    user_to_update = random.choice(st.session_state['bot_users'])
    st.session_state['user_scores'][user_to_update] += random.randint(1, 100)
    st.session_state['user_scores'][st.session_state['name']] = st.session_state['point_value']

    all_users = st.session_state['bot_users'] + [st.session_state['name']]
    random.shuffle(all_users)
    sorted_users = sorted([(user, st.session_state['user_scores'][user]) for user in all_users], key=lambda x: x[1], reverse=True)
    positions = [f"{i+1}{'st' if i == 0 else 'nd' if i == 1 else 'rd' if i == 2 else 'th'}" for i in range(len(sorted_users))]
    leaderboard_data = pd.DataFrame({
        'Position': positions,
        'Name': [user for user, score in sorted_users],
        'Score': [score for user, score in sorted_users],
        'Status': ["Good" if score > 400 else "Needs Improvement" for user, score in sorted_users]
    })
    st.session_state['leaderboard_data'] = leaderboard_data
    time.sleep(1)
    st.rerun()

def show_login_page():
    st.image(Image.open(background_path), use_column_width=True)
    st.title("EcoBreeze")
    name_input = st.text_input("QUICK LOGIN", "")
    if st.button("START"):
        if name_input.strip():
            st.session_state['name'] = name_input.strip()
            st.session_state['user_scores'][st.session_state['name']] = st.session_state['point_value']
            st.session_state['current_page'] = 'game'
            st.rerun()
        else:
            st.warning("Please enter your name!")

def show_game_page():
    st.image(Image.open(background_path), use_column_width=True)
    st.title(f"Welcome, {st.session_state['name']}")
    st.subheader(f"Points: {st.session_state['point_value']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.image(Image.open(ecobot_path).resize((200, 100)), caption="Talk to EcoBot", use_column_width=False, on_click=set_page, kwargs={'page': 'ecobot'}):
            pass
    with col2:
        if st.image(Image.open(ecoquest_path).resize((200, 100)), caption="Explore EcoQuests", use_column_width=False, on_click=set_page, kwargs={'page': 'ecoquest'}):
            pass

    pm25_status, pm25_color = get_pm25_status(st.session_state['pm25_value'])
    st.markdown(f"<h2 style='text-align: center;'>{st.session_state['pm25_value']} μg/m³ of PM2.5</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: {pm25_color};'>{pm25_status}</p>", unsafe_allow_html=True)

    st.subheader("LEADERBOARD")
    st.dataframe(st.session_state['leaderboard_data'])

    update_pm25()
    update_leaderboard()

def show_ecoquest_page():
    st.image(Image.open(background_path), use_column_width=True)
    if st.image(Image.open(back_path).resize((100, 50)), caption="Back to Game", use_column_width=False, on_click=set_page, kwargs={'page': 'game'}):
        pass
    st.title("EcoQuests")
    col1, col2 = st.columns(2)
    if col1.image(Image.open(level1_path).resize((200, 100)), caption="Plant a Tree!", use_column_width=False, on_click=set_page, kwargs={'page': 'task1'}):
        pass
    if col1.image(Image.open(level2_path).resize((200, 100)), caption="Listen to Calm Music!", use_column_width=False, on_click=set_page, kwargs={'page': 'task2'}):
        pass
    if col1.image(Image.open(level3_path).resize((200, 100)), caption="Turn off the Lights!", use_column_width=False, on_click=set_page, kwargs={'page': 'task3'}):
        pass
    if col2.image(Image.open(level4_path).resize((200, 100)), caption="Go for a Walk!", use_column_width=False, on_click=set_page, kwargs={'page': 'task4'}):
        pass
    if col2.image(Image.open(level5_path).resize((200, 100)), caption="Do some Exercise!", use_column_width=False, on_click=set_page, kwargs={'page': 'task5'}):
        pass

def show_task_page(task_number, task_description, points):
    st.image(Image.open(background_path), use_column_width=True)
    if st.image(Image.open(back_path).resize((100, 50)), caption="Back to EcoQuests", use_column_width=False, on_click=set_page, kwargs={'page': 'ecoquest'}):
        pass
    st.title(f"Task {task_number}")
    st.subheader(task_description)
    if st.image(Image.open(completed_path).resize((200, 100)), caption="Completed", use_column_width=False, on_click=task_completed, kwargs={'points': points}):
        pass

def task_completed(points):
    st.session_state['point_value'] += points
    st.image(Image.open(completed_tick_path).resize((200, 100)), caption="Task Completed!")
    time.sleep(1)
    st.session_state['current_page'] = 'ecoquest'
    st.rerun()

def show_ecobot_page():
    st.image(Image.open(background_path), use_column_width=True)
    if st.image(Image.open(back_path).resize((100, 50)), caption="Back to Game", use_column_width=False, on_click=set_page, kwargs={'page': 'game'}):
        pass
    st.title("EcoBot Chat")

    for sender, message in st.session_state['chat_log']:
        if sender == "You":
            with st.chat_message("user"):
                st.write(message)
        else:
            with st.chat_message("assistant"):
                st.write(message)

    if st.session_state['chat_sequence_index'] < len(chat_sequence):
        step = chat_sequence[st.session_state['chat_sequence_index']]
        if isinstance(step, tuple):
            sender, message = step
            st.session_state['chat_log'].append((sender, message))
            st.session_state['chat_sequence_index'] += 1
            st.rerun()
        elif isinstance(step, dict):
            columns = st.columns(len(step))
            keys = list(step.keys())
            for i, key in enumerate(keys):
                if columns[i].button(key):
                    st.session_state['chat_log'].append(("You", key))
                    response = step[key]
                    st.session_state['chat_log'].append(response)
                    st.session_state['chat_sequence_index'] += 1
                    st.session_state['chat_sequence_index'] = min(st.session_state['chat_sequence_index'], len(chat_sequence))
                    st.rerun()
    else:
        st.info("EcoBot is here to chat whenever you need!")

def set_page(page):
    st.session_state['current_page'] = page
    if page == 'ecobot' and not st.session_state['chat_log']:
        st.session_state['chat_sequence_index'] = 0
        step = chat_sequence[st.session_state['chat_sequence_index']]
        if isinstance(step, tuple):
            sender, message = step
            st.session_state['chat_log'].append((sender, message))
            st.session_state['chat_sequence_index'] += 1
    elif page != 'ecobot':
        st.session_state['chat_log'] = []
        st.session_state['chat_sequence_index'] = 0
    st.rerun()

# --- MAIN ---
if st.session_state['current_page'] == 'login':
    show_login_page()
elif st.session_state['current_page'] == 'game':
    show_game_page()
elif st.session_state['current_page'] == 'ecoquest':
    show_ecoquest_page()
elif st.session_state['current_page'] == 'task1':
    show_task_page(1, "Plant a tree!", random.randint(40, 100))
elif st.session_state['current_page'] == 'task2':
    show_task_page(2, "Listen to calm music!", random.randint(1, 20))
elif st.session_state['current_page'] == 'task3':
    show_task_page(3, "Turn off the lights!", random.randint(1, 10))
elif st.session_state['current_page'] == 'task4':
    show_task_page(4, "Go for a walk!", random.randint(100, 200))
elif st.session_state['current_page'] == 'task5':
    show_task_page(5, "Do some exercise!", random.randint(100, 200))
elif st.session_state['current_page'] == 'ecobot':
    show_ecobot_page()
