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
    .cookie-box {
        position: fixed;
        bottom: 20px;
        left: 20px;
        width: 300px;
        background-color: #fff8f4;
        border: 1px solid #ffc9b9;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0,0,0,0.1);
        z-index: 9999;
    }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- COOKIES HINWEIS ---
if "cookies_accepted" not in st.session_state:
    with st.container():
        st.markdown("""
        <div class="cookie-box">
            🍪 Diese Seite verwendet Cookies, um dein Nutzungserlebnis zu verbessern.<br><br>
        """, unsafe_allow_html=True)
        if st.button("Akzeptieren", key="cookie_btn"):
            st.session_state["cookies_accepted"] = True
            st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- LANDINGPAGE ---

st.image("https://instaupgrade.de/wp-content/uploads/2024/03/logo.svg", width=200)
st.title("InstaMaster – Smarter Instagram Bot für echtes Wachstum")

st.markdown("""
### 🚀 Automatisiere dein Wachstum auf Instagram – ganz ohne Fake-Follower!

- Echtes Engagement mit deiner Zielgruppe
- Interaktion mit ähnlichen Profilen
- Likes, Kommentare & Follows – komplett automatisiert
- Individuelle Zielgruppenanalyse basierend auf deinen Angaben
- DSGVO-konform, ohne Spam oder Bot-Gefahr
- Funktioniert ohne Werbung & ohne Facebook-Zugang

👉 **Wachse wie die Profis – sicher, smart und sichtbar.**

---
""")

# --- Testimonials ---
st.subheader("💬 Was sagen unsere Nutzer?")
st.success("\"Ich konnte mit InstaMaster in 2 Wochen über 800 echte Follower gewinnen – ohne Werbung!\" – Laura, Coachin")
st.info("\"Endlich ein Bot, der nicht spamt, sondern wirklich mit meiner Zielgruppe interagiert.\" – Tim, Content Creator")
st.success("\"Die automatische Zielgruppenanalyse hat mir so viel Zeit gespart – einfach genial!\" – Alex, Unternehmer")

st.markdown("**Jetzt starten & Abo aktivieren:**")
st.markdown("[🔐 Jetzt registrieren & Abo abschließen](https://www.checkout-ds24.com/product/599133)", unsafe_allow_html=True)

st.markdown("""
---
### 🔐 Du hast bereits ein Konto?
""")

email = st.text_input("E-Mail")
password = st.text_input("Passwort", type="password")

if email and password:
    if authenticate_user(email, password):
        st.success("✅ Login erfolgreich – Willkommen zurück!")

        st.markdown("[🧾 Mein Abo verwalten](https://www.digistore24.com/my/orders)", unsafe_allow_html=True)
        st.markdown("[🔓 Logout](#)", unsafe_allow_html=True)

        st.header("🔧 Bot-Zugang")
        st.write("Bitte gib deinen Instagram-Benutzernamen und dein Passwort ein.")
        ig_user = st.text_input("Instagram Benutzername")
        ig_pass = st.text_input("Instagram Passwort", type="password")

        if ig_user and ig_pass:
            client = login_instagram(ig_user, ig_pass)
            if client:
                st.success("🔐 Instagram Login erfolgreich")
                follower_count = client.user_info_by_username(ig_user).follower_count
                st.info(f"👥 Aktuelle Follower: {follower_count}")

                st.subheader("📌 Zielgruppen-Definition")
                target_description = st.text_area("Beschreibe deine Zielgruppe (z. B. Mütter mit Kleinkindern, Fitnessfans, Coaches)")
                competitor_profiles = st.text_input("Große Instagram-Profile mit ähnlicher Zielgruppe (z. B. @coachxy, @inspirationsdaily)")

                if st.button("🚀 Bot starten"):
                    current_hour = datetime.now().hour
                    if current_hour not in ACTIVE_HOURS:
                        st.warning("⏰ Der Bot ist aktuell im Nachtmodus (aktiv von 8–21 Uhr). Kein Start möglich.")
                    else:
                        settings = {
                            "ig_user": ig_user,
                            "target_description": target_description,
                            "competitor_profiles": competitor_profiles
                        }
                        save_settings(email, settings)
                        st.success("🌟 Einstellungen gespeichert. Der Bot arbeitet im Hintergrund.")

                        st.info("🤖 Bot analysiert jetzt Inhalte & Zielgruppenverhalten und interagiert eigenständig mit passenden Nutzern.")
    else:
        st.error("❌ Login fehlgeschlagen – bitte überprüfe deine Zugangsdaten.")
