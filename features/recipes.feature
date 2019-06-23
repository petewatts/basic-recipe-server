Feature: Recipes

  Scenario: As an API client I want to see a recipe's details
    Given I am an API client
    When I fetch a recipe by ID
    Then I can see recipe fields
