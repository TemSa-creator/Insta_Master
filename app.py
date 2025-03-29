app.py
import streamlit as st
import requests
import json

# --- CONFIG ---
TENTARY_API_KEY = " 968c63642c3ef2e43f76acb0e992715c"
TENTARY_PRODUCT_ID = "221551"

# --- PLACEHOLDER-FUNKTIONEN ---
def check_abo_status(user_email):
    # Hier simulieren wir die API-Abfrage bei Tentary
    # Du kannst das mit deinem echten API-Endpunkt ersetzen
    response = requests.get(
        f"https://api.tentary.com/subscription/status?email={user_email}&product_id={TENTARY_PRODUCT_ID}",
        headers={"Authorization": f"Bearer {TENTARY_API_KEY}"}
    )
    if response.status_code == 200:
        data = response.json()
        return data.get("active", False)
    return False

def save_settings(email, settings):
    # In einer echten Anwendung würdest du das in einer DB speichern
    with open(f"settings_{email}.json", "w") as f:
        json.dump(settings, f)

# --- UI ---
st.set_page_config(page_title="Insabot Plattform", page_icon="🚀")
st.title("🚀 Insabot – Deine automatisierte Insta-Wachstumsplattform")

st.write("Bitte gib deine E-Mail-Adresse ein, um deinen Abo-Status zu prüfen.")
email = st.text_input("E-Mail")

if email:
    if check_abo_status(email):
        st.success("✅ Abo aktiv – Dein Bot arbeitet im Hintergrund")

        st.header("🔧 Bot-Einstellungen")
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

        st.markdown("---")
        st.subheader("🎵 Zugang zum Musikbot")
        st.markdown("[Hier klicken, um deinen Musikbot zu starten](https://dein-musikbot-link.de)")

    else:
        st.error("❌ Kein aktives Abo gefunden. Bitte schließe zuerst dein Abo ab.")
        st.markdown("[Jetzt Abo abschließen](https://www.checkout-ds24.com/product/599133)")
