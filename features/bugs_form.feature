@qa-practice-full-challenge
Feature: QA Practice - Spot the Bugs Form (Complete Automation - All Possible Test Cases)
  As a senior QA automation engineer
  I want to validate every single aspect of the bugs-form page
  So that I automatically detect ALL intentional bugs + prove production-ready coverage

  # BACKGROUND - Ensures EVERY screenshot shows FILLED FORM + real state
  Background:
    Given I open the bugs form page
    And the page loads completely within 5 seconds
    When I fill the form with baseline valid data
    And I agree to terms and conditions

  # POSITIVE / HAPPY PATH SCENARIOS
  Scenario: POSITIVE 01 - Full valid submission works
    When I submit the form
    Then success message "Form submitted successfully!" is displayed
    And the success alert is green and dismissible

  Scenario: POSITIVE 02 - Exact minimum phone length (10 digits)
    When I enter phone number "1234567890"
    And I submit the form
    Then submission succeeds

  Scenario: POSITIVE 03 - Exact minimum password length (6 chars)
    When I enter password "Abc123"
    And I submit the form
    Then submission succeeds

  Scenario: POSITIVE 04 - Exact maximum password length (20 chars)
    When I enter password "Exact20CharPass1234!"
    And I submit the form
    Then submission succeeds

  Scenario: POSITIVE 05 - Country selection works
    When I select "New Zealand" from country dropdown
    And I submit the form
    Then submission succeeds

  # ==================================================================
  # NEGATIVE - MANDATORY FIELD VALIDATION (should block but don't)
  # ==================================================================
  Scenario: NEGATIVE 01 - Submit with empty Last Name
    When I clear Last Name
    And I submit the form
    Then success message appears anyway (BUG: mandatory field bypassed)

  Scenario: NEGATIVE 02 - Submit with empty Phone
    When I clear Phone
    And I submit the form
    Then success message appears anyway (BUG)

  Scenario: NEGATIVE 03 - Submit with empty Email
    When I clear Email
    And I submit the form
    Then success message appears anyway (BUG)

  Scenario: NEGATIVE 04 - Submit with empty Password
    When I clear Password
    And I submit the form
    Then success message appears anyway (BUG)

  Scenario: NEGATIVE 05 - Submit without agreeing to Terms
    When I uncheck terms and conditions
    And I submit_And I submit the form
    Then success message appears anyway (BUG: required checkbox bypassed)

  # ==================================================================
  # NEGATIVE - FORMAT VALIDATION FAILURES (no client-side enforcement)
  # ==================================================================
  Scenario: NEGATIVE 06 - Phone < 10 digits
    When I enter phone number "123456789"
    And I submit the form
    Then success message appears anyway (BUG: minlength=10 not enforced)

  Scenario: NEGATIVE 07 - Phone with letters
    When I enter phone number "021abc5678"
    And I submit the form
    Then success message appears anyway (BUG: no type=tel / pattern)

  Scenario: NEGATIVE 08 - Password < 6 chars
    When I enter password "Ab12"
    And I submit the form
    Then success message appears anyway (BUG: minlength=6 not in HTML)

  Scenario: NEGATIVE 09 - Password > 20 chars
    When I enter password "ThisPasswordIs21CharsLong"
    And I submit the form
    Then success message appears anyway (BUG: maxlength=20 missing)

  Scenario: NEGATIVE 10 - Invalid email format
    When I enter email "bad.email"
    And I submit the form
    Then success message appears anyway (BUG: no pattern or type enforcement)

  Scenario: NEGATIVE 11 - Email with spaces
    When I enter email "bad email@gmail.com"
    And I submit the form
    Then success message appears anyway (BUG)

  # ==================================================================
  # EDGE CASES - Boundaries & Special Input
  # ==================================================================
  Scenario: EDGE 01 - Phone exactly 10 digits with + and spaces
    When I enter phone number "+64 21 234 5678"
    And I submit the form
    Then submission succeeds

  Scenario: EDGE 02 - First Name 200 characters
    When I enter first name with 200 'A' characters
    And I submit the form
    Then submission succeeds

  Scenario: EDGE 03 - Special characters in names
    When I enter first name "O'Connor-Müller"
    And I enter last name "José Sánchez"
    And I submit the form
    Then submission succeeds

  Scenario: EDGE 04 - SQL injection attempt
    When I enter email "test'; DROP TABLE users;--@evil.com"
    And I submit the form
    Then no server error displayed (potential security risk)

  Scenario: EDGE 05 - XSS attempt in message
    When I enter message "<script>alert('XSS')</script>"
    And I submit the form
    Then no script execution on success page

  Scenario: EDGE 06 - Country left as default placeholder
    When I select "Select a country..." from country dropdown
    And I submit the form
    Then success message appears anyway (BUG: invalid country accepted)

  # ==================================================================
  # ALL Explicit detection
  # ==================================================================
  Scenario: BUG 01 - Phone label typo "nunber"
    Then phone label contains "nunber" instead of "number"

  Scenario: BUG 02 - Phone input type=text not tel
    Then phone input type is "text" not "tel"

  Scenario: BUG 03 - First Name missing required attribute
    Then first name input has no required attribute despite placeholder

  Scenario: BUG 04 - Terms checkbox required but no client validation
    Then terms checkbox has required attribute but form submits anyway

  Scenario: BUG 05 - Password label missing asterisk
    Then password label shows no asterisk despite being mandatory

  Scenario: BUG 06 - Phone missing minlength attribute
    Then phone input has no minlength attribute

  Scenario: BUG 07 - Password missing minlength/maxlength
    Then password input has no minlength or maxlength attributes

  Scenario: BUG 08 - Email missing pattern attribute
    Then email input has no pattern for validation

  Scenario: BUG 09 - Inconsistent asterisk usage
    Then only some mandatory fields have asterisk

  Scenario: BUG 10 - Note text contradicts reality
    Then note claims all * fields mandatory but First Name missing *

  Scenario: BUG 11 - Submit button says "Register"
    Then submit button text is "Register" not "Submit"

  Scenario: BUG 12 - Country default is placeholder
    Then country dropdown default is not a real country

  Scenario: BUG 13 - No proper form title
    Then page has no descriptive form title

  Scenario: BUG 14 - Phone placeholder vs label mismatch
    Then phone placeholder says "number" but label has "nunber"

  Scenario: BUG 15 - No visible error messages
    Then validation errors are completely silent

  Scenario: BUG 16 - Gender dropdown has no associated label
    Then gender select has no for/id linking

  Scenario: BUG 17 - Page not mobile responsive
    When I resize to 375px width
    Then sidebar overflows form content

  Scenario: BUG 18 - Success message not cleared on reload
    When I submit successfully
    And I reload the page
    Then success message still visible (should reset)

  # ==================================================================
  # PROFESSIONAL / REGRESSION / ACCESSIBILITY
  # ==================================================================
  Scenario: REGRESSION - Form resets after submission
    When I submit successfully
    Then all fields are cleared

  Scenario: ACCESSIBILITY - All inputs have labels
    Then every input has visible associated label except gender

  Scenario: SECURITY - Password field autocomplete off
    Then password field has autocomplete="new-password" or off

  Scenario: PERFORMANCE - Page load < 3 seconds
    Then full page load time is under 3 seconds

  # ==================================================================
  # DATA-DRIVEN EDGE CASES
  # ==================================================================
  Scenario Outline: DATA-DRIVEN - Phone number variations
    When I enter phone number "<phone>"
    And I submit the form
    Then submission "<expected>" (BUG analysis)

    Examples:
      | phone           | expected                  |
      | 123456789       | succeeds (BUG: too short) |
      | 12345678901     | succeeds (11 digits)      |
      | +64212345678    | succeeds                  |
      | 021 234 5678    | succeeds                  |
      | 0000000000      | succeeds (no logic)       |

  Scenario Outline: DATA-DRIVEN - Password edge lengths
    When I enter password "<password>"
    And I submit the form
    Then submission "<expected>"

    Examples:
      | password                  | expected                  |
      | Abc12                     | succeeds (BUG: 5 chars)   |
      | Abc123                    | succeeds                  |
      | Exact20CharPass1234!      | succeeds                  |
      | ThisIs21CharsLongPassword | succeeds (BUG: too long)  |

  Scenario Outline: DATA-DRIVEN - Email format extremes
    When I enter email "<email>"
    And I submit the form
    Then submission "<expected>"

    Examples:
      | email                          | expected                  |
      | a@b.c                          | succeeds                  |
      | test@toolongtld1234567890.com  | succeeds (TLD too long)   |
      | test@.com                      | succeeds (BUG)            |
      | test@com                       | succeeds (BUG)            |
      | user+tag@gmail.com             | succeeds                  |