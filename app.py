import streamlit as st
import requests
import json
from instagrapi import Client
import os
import random
from datetime import datetime

# --- CONFIG ---
ACTIVE_HOURS = range(8, 22)
USERS_DB = "users.json"

# --- USER MANAGEMENT ---
def load_users():
    if os.path.exists(USERS_DB):
        with open(USERS_DB, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_DB, "w") as f:
        json.dump(users, f)

def authenticate_user(email, password):
    users = load_users()
    if email in users and users[email]["password"] == password:
        return True
    return False

def save_settings(email, settings):
    with open(f"settings_{email}.json", "w") as f:
        json.dump(settings, f)

def login_instagram(username, password):
    cl = Client()
    session_file = f"session_{username}.json"
    if os.path.exists(session_file):
        cl.load_settings(session_file)
        try:
            cl.login(username, password)
        except Exception as e:
            st.error(f"Login mit gespeicherter Session fehlgeschlagen: {e}")
            return None
    else:
        try:
            cl.login(username, password)
            cl.dump_settings(session_file)
        except Exception as e:
            st.error(f"Login fehlgeschlagen: {e}")
            return None
    return cl

# --- STYLING MIT HINTERGRUND-BILD ---
st.set_page_config(page_title="InstaMaster", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    body {
        background-color: #fdf7f2;
        font-family: 'Helvetica Neue', sans-serif;
        background-image: url('https://i.postimg.cc/5Q4cjj59/instabot-bg.png');
        background-repeat: no-repeat;
        background-position: top left;
        background-size: 350px auto;
    }
    .css-18e3th9 { padding: 2rem 1rem; }
    .stButton>button {
        background-color: #ff3c69;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 0.75em 1.5em;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #e12f5b;
        transform: scale(1.02);
    }
    .stTextInput>div>input,
    .stTextArea>div>textarea {
        background-color: #fff8f4;
        padding: 0.6em;
        border-radius: 10px;
        border: 1px solid #ffc9b9;
    }
    .stSlider>div>div>div {
        background-color: #fde2d9;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ff3c69;
    }
    a {
        color: #ff3c69;
        font-weight: bold;
    }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- COOKIES HINWEIS ---
st.warning("🍪 Diese Seite verwendet Cookies, um dein Nutzungserlebnis zu verbessern.")

# --- REST BLEIBT UNVERÄNDERT (LANDINGPAGE + LOGIN ETC.) ---
# (Bleibt bestehen wie im bisherigen Code, hier nicht erneut eingefügt, um Übersicht zu wahren)
