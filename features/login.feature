Feature: User Login

    Scenario Outline: Login User
        Given User opens login page
        When Introduce credentials: email "<email>" and password "<password>".
        Then Login function working properly

        Examples:
            | email                | password           |
            | Input credentials    | Input credentials  |

