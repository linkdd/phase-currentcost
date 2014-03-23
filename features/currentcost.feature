Feature: data generation and sending
    As a developper,
    I want to generate and send fake data to NSCL,
    in order to test scalability and reliability of my projects

    Scenario Outline: Data generation and sending for SMEPI, ES and GridTeams not in real-time
        Given I generate data for <user_number> <project> user
        When I send data for <user_number> <project> user
        Then I should retrieve this data into NSCL for <user_number> <project> user

     Examples: Project
     | user_number | project   |
     | 1           | smepi     |
     | 50          | smepi     |
     | 1           | es        |
     | 20          | es        |
     | 1000        | es        |
     | 1           | gridteams |
     | 30          | gridteams |