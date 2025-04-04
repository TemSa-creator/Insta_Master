from playwright.sync_api import sync_playwright
import time
import random
from datetime import datetime

# --- Zeitfenster prüfen ---
current_hour = datetime.now().hour
if current_hour < 8 or current_hour > 21:
    print("⏰ Der Bot ist im Nachtmodus (aktiv nur von 8:00 bis 21:00 Uhr). Beende Ausführung.")
    exit()

# --- Bot starten mit gespeicherter Session ---
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=100)
    context = browser.new_context(storage_state="storage_state.json")
    page = context.new_page()

    print("🚀 Verwende gespeicherte Login-Session für Instagram...")

    page.goto("https://www.instagram.com/")
    time.sleep(random.uniform(3, 5))

    if "/accounts/login" in page.url:
        print("❌ Nicht eingeloggt – bitte zuerst save_session.py ausführen!")
        browser.close()
        exit()

    print("✅ Eingeloggt! Starte jetzt mit Interaktionen...")

    try:
        first_post = page.locator("article").first
        first_post.hover()
        time.sleep(random.uniform(1, 2))
        first_post.click()
        time.sleep(random.uniform(3, 4))
        like_button = page.locator("svg[aria-label='Gefällt mir']").first
        if like_button:
            like_button.click()
            print("❤️ Ersten Beitrag geliked!")
        else:
            print("⚠️ Kein Like-Button gefunden.")
    except Exception as e:
        print(f"⚠️ Fehler bei Interaktion mit Beitrag: {e}")

    browser.close()
