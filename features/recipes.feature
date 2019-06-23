Feature: Recipes

  Scenario: As an API client I want to see a recipe's details
    Given I am an API client
    When I fetch a recipe by ID
    Then I can see recipe fields

  Scenario: As an API client I want to see a paginated list of recipes by cuisine
    Given I am an API client
    When I fetch a recipe by cuisine
    Then I can see a list of recipes
    And the list is split into paginated results with 10 recipes per page
    And each recipe has to contain only the fields ID, title and description

  Scenario: As an API client I want to update one or more recipe's fields
    Given I am an API client
    When I update one or more recipes fields
    Then I can see the updated recipe fields
