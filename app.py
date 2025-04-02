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

# --- STYLE ---
st.set_page_config(page_title="InstaMaster", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    body { background-color: #fafafa; }
    .css-18e3th9 { padding: 2rem 1rem; }
    .stButton>button {
        background-color: #ff5c5c;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.75em 1.5em;
    }
    .stTextInput>div>input {
        background-color: #fff;
        padding: 0.6em;
        border-radius: 10px;
        border: 1px solid #ccc;
    }
    .stSlider>div>div>div {
        background-color: #f3f3f3;
    }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- COOKIES HINWEIS ---
st.warning("🍪 Diese Seite verwendet Cookies, um dein Nutzungserlebnis zu verbessern.")

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
