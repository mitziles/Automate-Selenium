Feature: Add elements in cart

    Scenario Outline: Add 2 different items in cart and check if they are added to cart
        Given User opens the home page.
        When User searches for "<parfume1>" and "<parfume2>" and adds them to cart.
        Then Checks if the "<parfume1>" and "<parfume2>" are added in cart.

        Examples:
            | parfume1                | parfume2               |
            | Versace Eros            | Paco Rabanne Invictus  |
