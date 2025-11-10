# environment.py

import os
from playwright.sync_api import sync_playwright

def before_all(context):
    """Setup: Launch Playwright and browser once"""
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(
        headless=False,      # Visible for demo purposes
        slow_mo=700          # Slow down for observation
    )
    # Auto-create screenshots folder
    os.makedirs("screenshots", exist_ok=True)
    print("\n" + "═" * 70)
    print("🚀 PLAYWRIGHT BROWSER LAUNCHED - BDD TESTS READY")
    print("📸 Screenshots will be saved automatically on ANY failure")
    print("═" * 70 + "\n")


def before_scenario(context, scenario):
    """Run before each scenario: fresh page + navigation"""
    context.page = context.browser.new_page()
    context.page.set_viewport_size({"width": 1920, "height": 1080})
    
    try:
        context.page.goto(
            "https://qa-practice.netlify.app/bugs-form",
            wait_until="networkidle",
            timeout=30000
        )
        print(f"✅ Starting scenario: {scenario.name}")
    except Exception as e:
        print(f"❌ Failed to load page: {e}")


def after_scenario(context, scenario):
    """Run after each scenario: Screenshot on fail + safe cleanup"""
    screenshot_taken = False
    
    if scenario.status == "failed":
        # Safe filename (no invalid chars)
        safe_name = "".join(
            c if c.isalnum() or c in " _-()" else "_"
            for c in scenario.name
        )[:150]
        path = f"screenshots/{safe_name}.png"
        
        print(f"\n❌ SCENARIO FAILED: {scenario.name}")
        
        # MAIN screenshot attempt
        try:
            context.page.screenshot(
                path=path,
                full_page=True,
                timeout=30000
            )
            print(f"📸 BUG PROOF SAVED → {path}")
            screenshot_taken = True
        except Exception as e:
            print(f"⚠️ Main screenshot failed: {e}")
        
        # FALLBACK: Try any open page in context
        if not screenshot_taken:
            try:
                pages = context.browser.contexts[0].pages
                if pages:
                    pages[0].screenshot(path=path.replace(".png", "_FALLBACK.png"), full_page=True)
                    print(f"📸 FALLBACK screenshot saved!")
                    screenshot_taken = True
            except:
                pass
        
        if not screenshot_taken:
            print("🚨 CRITICAL: Screenshot completely failed - page likely crashed")

    else:
        print(f"✅ Scenario PASSED: {scenario.name}")

    # Always close page safely
    try:
        context.page.close()
    except:
        pass


def after_all(context):
    """Cleanup: Close everything and show results"""
    try:
        context.browser.close()
    except:
        pass
    try:
        context.playwright.stop()
    except:
        pass
    
    # Count screenshots
    if os.path.exists("screenshots"):
        count = len([f for f in os.listdir("screenshots") if f.endswith(".png")])
    else:
        count = 0
    
    print("\n" + "═" * 70)
    print("🏁 ALL TESTS COMPLETED")
    print(f"📁 Screenshots folder: ./{'screenshots' if count > 0 else 'screenshots (empty)'}")
    print(f"🖼️  Total bug proof screenshots: {count}")
    if count > 0:
        print("🎯 You found real bugs! Show these PNGs in the interview!")
    print("═" * 70 + "\n")