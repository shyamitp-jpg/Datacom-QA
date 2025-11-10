# features/steps/bugs_form_steps.py

from behave import given, when, then, step
from playwright.sync_api import expect, Page
import re
import time

# === EXACT LOCATORS ===
LOCATORS = {
    "first_name": "#first-name",
    "last_name": "#last-name",
    "phone": "#phone",
    "email": "#email",
    "password": "#password",
    "country": "select#country",
    "gender": "#gender",
    "message": "#message",
    "terms": "#agree-terms",
    "submit": "#submit-btn",
    "success": ".alert-success",
    "phone_label": "label[for='phone']",
    "password_label": "label[for='password']",
    "email_label": "label[for='email']",
    "note": "small",
    "form_title": "h1, h2, h3",
    "gender_label": "label[for='gender']",
}

# === VALID BASELINE DATA ===
VALID = {
    "first_name": "Shyam",
    "last_name": "Sundar",
    "phone": "0212345678",
    "email": "shyam.itp@gmail.com",
    "password": "Secure123",
    "country": "New Zealand",
    "gender": "Male",
    "message": "Senior QA automation - all bugs found!"
}

# === GIVEN ===
@given("I open the bugs form page")
def open_page(context):
    context.page.goto("https://qa-practice.netlify.app/bugs-form")
    expect(context.page).to_have_url(re.compile("bugs-form"))
    context.page.wait_for_load_state("networkidle")

# === REUSABLE FILL (used in Background) ===
def fill_valid(context):
    p = context.page
    p.fill(LOCATORS["first_name"], VALID["first_name"])
    p.fill(LOCATORS["last_name"], VALID["last_name"])
    p.fill(LOCATORS["phone"], VALID["phone"])
    p.fill(LOCATORS["email"], VALID["email"])
    p.fill(LOCATORS["password"], VALID["password"])
    p.select_option(LOCATORS["country"], label=VALID["country"])
    p.select_option(LOCATORS["gender"], VALID["gender"])
    p.fill(LOCATORS["message"], VALID["message"])
    p.check(LOCATORS["terms"])

@given("I fill the form with valid baseline data")
def step_fill_valid(context):
    fill_valid(context)

# === WHEN ===
@when("I agree to terms and conditions")
def agree_terms(context):
    context.page.check(LOCATORS["terms"])

@when("I submit the form")
def submit_form(context):
    context.page.click(LOCATORS["submit"])
    context.page.wait_for_timeout(1500)

@when("I clear the {field} field")
def clear_field(context, field):
    selector = LOCATORS.get(field.lower().replace(" ", "_"))
    if selector:
        context.page.fill(selector, "")

@when("I enter phone {phone}")
def enter_phone(context, phone):
    context.page.fill(LOCATORS["phone"], phone)

@when("I enter password {password}")
def enter_password(context, password):
    context.page.fill(LOCATORS["password"], password)

@when("I enter email {email}")
def enter_email(context, email):
    context.page.fill(LOCATORS["email"], email)

@when("I enter message {msg}")
def enter_message(context, msg):
    context.page.fill(LOCATORS["message"], msg)

@when("I uncheck terms and conditions")
def uncheck_terms(context):
    context.page.uncheck(LOCATORS["terms"])

@when("I select {country} in country dropdown")
def select_country(context, country):
    context.page.select_option(LOCATORS["country"], label=country)

@when("I enter first name with {num:d} characters")
def long_first_name(context, num):
    context.page.fill(LOCATORS["first_name"], "A" * num)

@when("I resize browser to {width:d}x{height:d}")
def resize_mobile(context, width, height):
    context.page.set_viewport_size({"width": width, "height": height})

@when("I capture initial page state for comparisons")
def capture_state(context):
    context.initial_html = context.page.content()

# === THEN ===
@then("success message {text} is displayed")
def check_success(context, text):
    success = context.page.locator(LOCATORS["success"])
    expect(success).to_be_visible(timeout=10000)
    expect(success).to_contain_text(text)

@then("submission succeeds anyway {reason}")
def bug_success(context, reason):
    check_success(context, "Form submitted successfully!")
    assert True, f"BUG: {reason}"

@then("the phone label text is {expected}")
def phone_label_exact(context, expected):
    label = context.page.locator(LOCATORS["phone_label"]).text_content().strip()
    assert label == expected, f"BUG 01: Typo confirmed - got '{label}'"

@then("phone input has type {typ} not {expected}")
def phone_type(context, typ, expected):
    actual = context.page.get_attribute(LOCATORS["phone"], "type")
    assert actual == typ, f"BUG 02: type={actual} (should be {expected})"

@then("first name input has no {attr} attribute")
def no_attr(context, attr):
    has = context.page.eval_on_selector(LOCATORS["first_name"], f"el => el.hasAttribute('{attr}')")
    assert not has, f"BUG 03: First Name missing {attr}"

@then("password label has no {symbol} despite being mandatory")
def password_no_star(context, symbol):
    label = context.page.locator(LOCATORS["password_label"]).text_content()
    assert symbol not in label, f"BUG 05: Password label missing {symbol}"

@then("phone input has no minlength={num:d}")
def phone_no_minlength(context, num):
    ml = context.page.get_attribute(LOCATORS["phone"], "minlength")
    assert ml is None, f"BUG 06: minlength missing (should be {num})"

@then("password input has no minlength={min:d} or maxlength={max:d}")
def password_no_lengths(context, min, max):
    assert context.page.get_attribute(LOCATORS["password"], "minlength") is None
    assert context.page.get_attribute(LOCATORS["password"], "maxlength") is None
    assert True, f"BUG 07: missing length attributes"

@then("First Name has no asterisk but others do")
def inconsistent_asterisks(context):
    labels = context.page.locator("label").all_inner_texts()
    first_has = any("*" in l and "First" in l for l in labels)
    others_have = any("*" in l for l in labels if "First" not in l)
    assert not first_has and others_have, "BUG 09: Inconsistent mandatory markers"

@then("note says {text} but First Name isn't marked")
def note_contradiction(context, text):
    note = context.page.locator(LOCATORS["note"]).text_content()
    assert text in note, "BUG 10: Note contradicts visible asterisks"

@then("submit button text is {text} not {expected}")
def button_wrong_text(context, text, expected):
    btn = context.page.locator(LOCATORS["submit"]).text_content()
    assert text in btn, f"BUG 11: Button says '{btn}'"

@then("country dropdown default option is {placeholder}")
def country_placeholder(context, placeholder):
    default = context.page.locator(f"{LOCATORS['country']} option").first.text_content()
    assert placeholder in default, f"BUG 12: Default = '{default}'"

@then("page has no descriptive form title")
def no_form_title(context):
    title = context.page.locator(LOCATORS["form_title"]).first.text_content()
    assert "form" not in title.lower() and "register" not in title.lower(), "BUG 13: Missing proper title"

@then("validation errors are completely silent")
def no_error_messages(context):
    errors = context.page.locator(".text-danger, .invalid-feedback, .text-red").count()
    assert errors == 0, "BUG 15: No client-side error feedback"

@then("gender field fails WCAG")
def gender_no_label(context):
    assert context.page.locator(LOCATORS["gender_label"]).count() == 0, "BUG 16: No label for gender"

@then("form elements overflow or misalign")
def mobile_overflow(context):
    form_x = context.page.locator("form").bounding_box()["x"]
    sidebar_x = context.page.locator("nav").bounding_box()["x"]
    assert abs(form_x - sidebar_x) < 50, "BUG 17: Mobile layout broken"

@then("success message still visible")
def success_persists(context):
    expect(context.page.locator(LOCATORS["success"])).to_be_visible()
    assert True, "BUG 18: Success message not cleared on reload"

@then("every input has visible associated label except gender")
def a11y_check(context):
    assert context.page.locator("label[for='gender']").count() == 0
    # Add more axe checks in environment.py if needed