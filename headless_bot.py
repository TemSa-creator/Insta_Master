import sys
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright

# --- CLI Argumente lesen ---
username = sys.argv[1] if len(sys.argv) > 1 else ""
password = sys.argv[2] if len(sys.argv) > 2 else ""

if not username or not password:
    print("Fehlende Login-Daten")
    sys.exit(1)

# --- Zeitfenster prüfen ---
current_hour = datetime.now().hour
if current_hour < 8 or current_hour > 21:
    print("⏰ Der Bot ist im Nachtmodus (aktiv nur von 8:00 bis 21:00 Uhr). Beende Ausführung.")
    sys.exit(0)

# --- Bot starten ---
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=100)
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")
    page = context.new_page()

    print(f"🔐 Starte Instagram-Login für {username}...")

    page.goto("https://www.instagram.com/accounts/login/")
    time.sleep(random.uniform(2.5, 4.0))

    # Cookies akzeptieren
    try:
        page.click("text=Alle zulassen")
    except:
        pass

    # Login-Felder ausfüllen
    try:
        page.wait_for_selector("input[name='username']", timeout=30000)
        username_field = page.query_selector("input[name='username']")
        password_field = page.query_selector("input[name='password']")

        if not username_field or not password_field:
            raise Exception("Login-Felder nicht gefunden")

        username_field.fill(username)
        time.sleep(random.uniform(0.8, 1.2))
        password_field.fill(password)
        time.sleep(random.uniform(1.0, 2.0))

    except Exception as e:
        print(f"⚠️ Fehler beim Finden oder Ausfüllen der Login-Felder: {e}")
        browser.close()
        sys.exit(1)

    # Sicherer Login-Klick
    try:
        page.wait_for_selector("button[type='submit']", timeout=15000)
        submit_button = page.query_selector("button[type='submit']")
        if submit_button:
            page.evaluate("el => el.scrollIntoView()", submit_button)
            time.sleep(random.uniform(0.8, 1.4))
            try:
                submit_button.click()
            except:
                print("⚠️ Normaler Klick fehlgeschlagen – versuche Force-Click...")
                page.click("button[type='submit']", force=True)
        else:
            raise Exception("🚫 Login-Button nicht gefunden!")
    except Exception as e:
        print(f"⚠️ Sicherer Klick auf Login-Button fehlgeschlagen: {e}")
        browser.close()
        sys.exit(1)

    time.sleep(random.uniform(5, 7))

    if "challenge" in page.url or "two_factor" in page.url:
        print("🔐 Zwei-Faktor oder Challenge erkannt – Bot kann nicht fortfahren.")
    elif "/accounts/" in page.url:
        print("✅ Login erfolgreich! Starte jetzt mit Interaktionen...")

        page.goto("https://www.instagram.com/")
        time.sleep(random.uniform(4, 6))

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
            print(f"⚠️ Keine Posts gefunden oder Like nicht möglich: {e}")
    else:
        print("❌ Login fehlgeschlagen – bitte Zugangsdaten überprüfen.")

    browser.close()
