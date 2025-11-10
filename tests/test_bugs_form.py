import re
from pathlib import Path
from playwright.sync_api import Page, expect
import pytest

BASE_URL = "https://qa-practice.netlify.app/bugs-form"

@pytest.mark.ui
def test_successful_bug_submission_with_file(page: Page, tmp_path: Path):
    page.goto(BASE_URL)

    # Fill all fields
    page.get_by_label(re.compile("First Name", re.I)).fill("Shyam")
    page.get_by_label(re.compile("Last Name", re.I)).fill("Sundar")
    page.get_by_label(re.compile("Email", re.I)).fill("shyam.itp@gmail.com")
    page.get_by_label(re.compile("Mobile|Phone", re.I)).fill("0212345678")

    bug_type = page.get_by_label(re.compile("Bug Type|Category", re.I))
    if bug_type.is_visible():
        bug_type.select_option(index=1)

    page.get_by_label(re.compile("Bug description", re.I)).fill(
        "Steps:\n1. Open bug form\n2. Fill details\n3. Submit\nExpected: Confirmation message."
    )

    dummy_file = tmp_path / "bug-log.txt"
    dummy_file.write_text("Sample bug log content for upload.")
    file_input = page.locator("input[type='file']")
    if file_input.is_visible():
        file_input.set_input_files(str(dummy_file))

    page.get_by_role("button", name=re.compile("submit", re.I)).click()
    expect(page.get_by_text(re.compile("thank you|submitted", re.I))).to_be_visible()
