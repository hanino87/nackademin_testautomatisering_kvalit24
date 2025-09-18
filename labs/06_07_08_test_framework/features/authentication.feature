Feature: User Signup and Login authentication  

  Scenario: New user can sign up and log in successfully
    Given a new user with a unique username and password
    When the user signs up via the UI
    And the user logs in via the UI
    Then the user should see a personalized welcome message

