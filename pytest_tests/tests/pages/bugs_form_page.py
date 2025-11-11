from playwright.sync_api import Page
import time

class BugsFormPage:
    def __init__(self, page: Page):
        self.page = page
        self.page.goto("https://qa-practice.netlify.app/bugs-form")
        self.page.wait_for_load_state("networkidle")

    def slow_fill(self):
        def type_it(sel, text):
            self.page.click(sel)
            self.page.fill(sel, "")
            for c in text:
                self.page.keyboard.type(c)
                time.sleep(0.08)
        type_it("#firstName", "Shyam")
        type_it("#lastName", "Sundar")
        type_it("#phone", "0212345678")
        type_it("#emailAddress", "Shyamin@example.com")
        type_it("#password", "2025Test")
        self.page.select_option("#countries_dropdown_menu", "New Zealand")
        #self.page.check("#exampleCheck1")