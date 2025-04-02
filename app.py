import streamlit as st
import requests
import json
from instagrapi import Client
import os

# --- CONFIG ---
TENTARY_API_KEY = " 968c63642c3ef2e43f76acb0e992715c"
TENTARY_PRODUCT_ID = "221551"

# --- PLACEHOLDER-FUNKTIONEN ---
def check_abo_status(user_email):
    response = requests.get(
        f"https://api.tentary.com/subscription/status?email={user_email}&product_id={TENTARY_PRODUCT_ID}",
        headers={"Authorization": f"Bearer {TENTARY_API_KEY}"}
    )
    if response.status_code == 200:
        data = response.json()
        return data.get("active", False)
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

# --- UI ---
st.set_page_config(page_title="Insabot Plattform", page_icon="🚀")
st.title("🚀 Instabot – Deine automatisierte Insta-Wachstumsplattform")

st.write("Bitte gib deine E-Mail-Adresse ein, um deinen Abo-Status zu prüfen.")
email = st.text_input("E-Mail")

if email:
    if check_abo_status(email):
        st.success("✅ Abo aktiv – Dein Bot arbeitet im Hintergrund")

        st.header("🔧 Bot-Einstellungen")
        st.write("Bitte gib deine Instagram-Zugangsdaten ein (werden NICHT dauerhaft gespeichert)")
        ig_user = st.text_input("Instagram Benutzername")
        ig_pass = st.text_input("Instagram Passwort", type="password")

        if ig_user and ig_pass:
            client = login_instagram(ig_user, ig_pass)
            if client:
                st.success("🔐 Instagram Login erfolgreich")

                hashtags = st.text_input("Ziel-Hashtags (mit Komma getrennt)")
                profiles = st.text_input("Zielprofile (z. B. @coachxy, @businessqueen)")
                likes = st.slider("Likes pro Tag", 10, 200, 50)
                comments = st.checkbox("Kommentare aktivieren")
                dms = st.checkbox("DMs an neue Follower senden")

                if st.button("📁 Einstellungen speichern & Bot starten"):
                    settings = {
                        "hashtags": hashtags,
                        "profiles": profiles,
                        "likes": likes,
                        "comments": comments,
                        "dms": dms
                    }
                    save_settings(email, settings)
                    st.success("🌟 Einstellungen gespeichert. Dein Bot ist aktiv.")

                    # --- SIMPLE LIKE-FUNKTION NACH HASHTAGS (als Start!) ---
                    if hashtags:
                        st.info("🔄 Bot startet Like-Runde...")
                        for tag in [h.strip() for h in hashtags.split(",") if h.strip()]:
                            medias = client.hashtag_medias_recent(tag, amount=likes//len(hashtags.split(",")))
                            for media in medias:
                                try:
                                    client.media_like(media.id)
                                except:
                                    pass
                        st.success("✅ Likes wurden verteilt!")

                st.markdown("---")
                st.subheader("🎵 Zugang zum Musikbot")
                st.markdown("[Hier klicken, um deinen Musikbot zu starten](https://dein-musikbot-link.de)")

    else:
        st.error("❌ Kein aktives Abo gefunden. Bitte schließe zuerst dein Abo ab.")
        st.markdown("[Jetzt Abo abschließen](https://www.checkout-ds24.com/product/599133)")
