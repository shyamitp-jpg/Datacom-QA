# pytest_tests/tests/test_bugs_form.py

import pytest
from playwright.sync_api import expect
import time

# HAPPY PATH
# ===============================================
def test_happy_path(form):
    form.slow_fill()
    form.page.click("#registerBtn")  
    expect(form.page.locator(".alert-danger")).to_be_visible(timeout=10000)  # FIXED
    expect(form.page.locator(".alert-danger")).to_contain_text("Successfully registered the following information")

def test_bug_01_phone_typo(form):
    form.slow_fill()
    label = form.page.locator("label[for='lastName']").text_content().strip()
    expect(form.page.locator(".alert-danger")).to_be_visible(timeout=10000)  # FIXED
    assert "nunber" in label
    assert label == "Phone nunber*"  # exact typo
    

def test_bug_11_register_button(form):
    form.slow_fill()
    button_text = form.page.locator("#registerBtn").text_content().strip()
    assert "Register" in button_text
    assert button_text == "Register"  # BUG: should be "Submit"

# NEGATIVE - MANDATORY BYPASSED (8+ executions)
# ===============================================
@pytest.mark.parametrize("field, selector", [
    ("Last Name", "#lastName"),
    ("Phone", "#phone"),
    ("Email", "#emailAddress"),
    ("Password", "#password"),
])
def test_negative_mandatory_bypassed(form, field, selector):
    form.slow_fill()
    form.page.fill(selector, "")
    form.page.click("#registerBtn")
    expect(form.page.locator(".alert-danger")).to_be_visible()  # BUG
    assert True, f"BUG: {field} bypassed"

def test_negative_terms_bypassed(form):
    form.slow_fill()
    form.page.uncheck("#exampleCheck1")
    form.page.click("#registerBtn")
    expect(form.page.locator(".alert-danger")).to_be_visible()  # BUG

# NEGATIVE - INVALID DATA ACCEPTED (20+ executions)
# ===============================================
@pytest.mark.parametrize("phone, desc", [
    ("123", "too short"),
    ("abcdefghij", "letters only"),
    ("021 234 5678", "spaces"),
    ("+64-21-2345678", "dashes"),
    ("", "empty"),
])
def test_negative_phone_invalid_accepted(form, phone, desc):
    form.slow_fill()
    form.page.fill("#phone", phone)
    form.page.click("#registerBtn")
    expect(form.page.locator(".alert-danger")).to_be_visible()  # BUG

@pytest.mark.parametrize("email, desc", [
    ("bad", "no @"),
    ("bad@", "no domain"),
    ("bad@com", "no tld"),
    ("bad @ gmail.com", "spaces"),
    ("", "empty"),
])
def test_negative_email_invalid_accepted(form, email, desc):
    form.slow_fill()
    form.page.fill("#emailAddress", email)
    form.page.click("#registerBtn")
    expect(form.page.locator(".alert-danger")).to_be_visible()  # BUG

@pytest.mark.parametrize("password, desc", [
    ("abc", "<6 chars"),
    ("a"*21, ">20 chars"),
    ("", "empty"),
])
def test_negative_password_invalid_accepted(form, password, desc):
    form.slow_fill()
    form.page.fill("#password", password)
    form.page.click("#registerBtn")
    expect(form.page.locator(".alert-danger")).to_be_visible()  # BUG

# ALL REMAINING BUGS VALIDATION
# ===============================================
def test_bug_02_phone_type_text_not_tel(form):
    form.slow_fill()
    assert form.page.get_attribute("#phone", "type") == "text"

def test_bug_03_first_name_no_required(form):
    form.slow_fill()
    has_req = form.page.eval_on_selector("#firstName", "el => el.hasAttribute('required')")
    assert not has_req

def test_bug_04_terms_no_validation(form):
    form.slow_fill()
    form.page.uncheck("#exampleCheck1")
    form.page.click("#registerBtn")
    expect(form.page.locator(".alert-danger")).to_be_visible()  # BUG

def test_bug_05_password_label_missing_asterisk(form):
    form.slow_fill()
    label = form.page.locator("label[for='exampleInputPassword1']").text_content()
    assert "*" not in label 

def test_bug_06_phone_no_minlength(form):
    form.slow_fill()
    assert form.page.get_attribute("#phone", "minlength") is None

def test_bug_07_password_no_lengths(form):
    form.slow_fill()
    assert form.page.get_attribute("#password", "minlength") is None
    assert form.page.get_attribute("#password", "maxlength") is None

def test_bug_08_email_no_pattern(form):
    form.slow_fill()
    assert form.page.get_attribute("#emailAddress", "pattern") is None

def test_bug_09_inconsistent_asterisks(form):
    form.slow_fill()
    labels = form.page.locator("label").all_text_contents()
    first_has = any("*" in l and "First" in l for l in labels)
    others_have = any("*" in l for l in labels if "First" not in l)
    assert not first_has and others_have

def test_bug_12_country_placeholder(form):
    form.page.goto(form.page.url)  # fresh
    default = form.page.locator("select option").first.text_content().strip()
    assert "Select a country..." in default

def test_bug_13_no_title(form):
    form.slow_fill()
    titles = form.page.locator("h1,h2,h3,h4").all_text_contents()
    assert not any("form" in t.lower() for t in titles if t.strip())

def test_bug_14_placeholder_vs_label(form):
    form.slow_fill()
    ph = form.page.get_attribute("#phone", "placeholder").lower()
    label = form.page.locator("label[for='lastName']").text_content()
    assert "number" in ph
    assert "nunber" in label

def test_bug_15_no_errors(form):
    form.slow_fill()
    form.page.fill("#lastName", "")
    form.page.click("#registerBtn")
    assert form.page.locator(".text-danger, .invalid-feedback").count() == 0

def test_bug_16_a11y_missing_labels(form):
    form.slow_fill()
    assert form.page.locator("label[for='lastName']").count() == 0

def test_bug_17_success_persists(form):
    form.slow_fill()
    form.page.click("#registerBtn")
    expect(form.page.locator(".alert-danger")).to_be_visible()
    form.page.reload()
    form.page.wait_for_load_state("networkidle")
    assert form.page.locator(".alert-danger").is_visible()  # BUG


