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
    browser = p.chromium.launch(headless=True, slow_mo=100)  # Slow mode für menschlich wirkende Aktionen
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")
    page = context.new_page()

    print(f"🔐 Starte Instagram-Login für {username}...")

    page.goto("https://www.instagram.com/accounts/login/")
    time.sleep(random.uniform(2.5, 4.0))

    # Cookies akzeptieren, falls vorhanden
    try:
        page.click("text=Alle zulassen")
    except:
        pass

    # Login-Felder ausfüllen
    page.fill("input[name='username']", username)
    time.sleep(random.uniform(0.8, 1.2))
    page.fill("input[name='password']", password)
    time.sleep(random.uniform(1.0, 2.0))

    # Neuer robuster Klick mit evaluateHandle (bypasst Blockierungen)
    try:
        login_button = page.query_selector("button[type='submit']")
        if login_button:
            page.evaluate("element => element.click()", login_button)
        else:
            print("❌ Login-Button nicht gefunden.")
            browser.close()
            sys.exit(1)
    except Exception as e:
        print(f"⚠️ Fehler beim Klick auf Login: {e}")
        browser.close()
        sys.exit(1)

    time.sleep(random.uniform(5, 7))

    # Login erfolgreich?
    if "challenge" in page.url or "two_factor" in page.url:
        print("🔐 Zwei-Faktor oder Challenge erkannt – Bot kann nicht fortfahren.")
    elif "/accounts/" in page.url:
        print("✅ Login erfolgreich! Starte jetzt mit Interaktionen...")

        # Gehe zur Startseite
        page.goto("https://www.instagram.com/")
        time.sleep(random.uniform(4, 6))

        try:
            first_post = page.locator("article").first
            first_post.hover()
            time.sleep(random.uniform(1, 2))
            first_post.click()
            time.sleep(random.uniform(3, 4))
            page.click("svg[aria-label='Gefällt mir']")
            print("❤️ Ersten Beitrag geliked!")
        except Exception as e:
            print(f"⚠️ Keine Posts gefunden oder Like nicht möglich: {e}")

    else:
        print("❌ Login fehlgeschlagen – bitte Zugangsdaten überprüfen.")

    browser.close()
