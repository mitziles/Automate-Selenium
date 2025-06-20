Feature: User Register

    Scenario Outline: Register new User
        Given User opens login page and wants to create a new account
        When Introduce credentials: email "<email>" and password "<password>"
        Then Register succesful

        Examples:
            | email                | password           |
            | Input credentials    | Input credentials  |