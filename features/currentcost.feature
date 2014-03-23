Feature: Current Cost data collection
    As a end-user,
    I want to see my current cost information about my consumption,
    in order to reduce my energy consumption

    Scenario Outline: Missing argument
        When we launch currentcost script without important argument
        Then we should see an error message on screen and in log

    Scenario Outline: Bad argument value
        When we launch currentcost script with a bad value for an argument
        Then we should see an error message on screen and in log

    Scenario Outline: Problem with current cost connexion
        Given current cost is unreachable
        When we launch currentcost script
        Then we should receive a message over the network saying that current cost is unreachable
        And we should see this error in log

    Scenario Outline: Problem with current cost disconnection
        Given current cost is disconnected
        When we launch currentcost script
        Then we should receive an error message over the network saying that current cost is disconnected
        And we should see this error in log

    Scenario Outline: Problem with current cost message
        Given current cost is connected but send incorrect message
        When we launch currentcost script
        Then We should see this error in log

    Scenario Outline: Problem with USB port
        Given current cost is connected and currentcost script is launched
        When we disconnect USB port
        Then we should receive and error message over the network
        And we should see this error in log

    Scenario Outline: Nominal case
        Given current cost is connected
        When we launch currentcost script
        Then we should receive a success message over the network
