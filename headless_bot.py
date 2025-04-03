import sys
import time
from playwright.sync_api import sync_playwright

# --- CLI Argumente lesen ---
username = sys.argv[1] if len(sys.argv) > 1 else ""
password = sys.argv[2] if len(sys.argv) > 2 else ""

if not username or not password:
    print("Fehlende Login-Daten")
    sys.exit(1)

# --- Bot starten ---
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    print(f"🔐 Starte Instagram-Login für {username}...")

    page.goto("https://www.instagram.com/accounts/login/")
    time.sleep(3)

    # Cookies akzeptieren, falls vorhanden
    try:
        page.click("text=Alle zulassen")
    except:
        pass

    # Login-Felder ausfüllen
    page.fill("input[name='username']", username)
    page.fill("input[name='password']", password)

    # Sicherer Klick auf Login-Button mit JavaScript-Bypass
    try:
        page.evaluate("document.querySelector('button[type=\\'submit\\']').click()")
    except Exception as e:
        print(f"⚠️ Fehler beim Klick auf Login: {e}")
        browser.close()
        sys.exit(1)

    time.sleep(5)

    # Login erfolgreich?
    if "challenge" in page.url or "two_factor" in page.url:
        print("🔐 Zwei-Faktor oder Challenge erkannt – Bot kann nicht fortfahren.")
    elif "/accounts/" in page.url:
        print("✅ Login erfolgreich! Starte jetzt mit Interaktionen...")

        # Beispiel: Gehe zu Startseite und like einen Beitrag
        page.goto("https://www.instagram.com/")
        time.sleep(5)

        try:
            first_post = page.locator("article").first
            first_post.hover()
            first_post.click()
            time.sleep(3)
            page.click("svg[aria-label='Gefällt mir']")
            print("❤️ Ersten Beitrag geliked!")
        except Exception as e:
            print(f"Keine Posts gefunden oder Like nicht möglich: {e}")

    else:
        print("❌ Login fehlgeschlagen – bitte Zugangsdaten überprüfen.")

    browser.close()
