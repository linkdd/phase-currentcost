Feature: Current Cost data collection
    As a end-user,
    I want to see my current cost information about my consumption,
    in order to reduce my energy consumption

    Scenario: Missing argument
        When we launch currentcost script without important argument
        Then we should see an error message on screen

    Scenario: Problem with current cost connexion without RabbitMQ
        When we start currentcost with bad port without rabbitmq
        Then we should see currentcost is unreachable in log

    Scenario: Problem with RabbitMQ credential
        When we start currentcost with bad port and bad rabbitmq credential
        Then we should see currentcost is unreachable in log
        And we should see rabbitmq error in log

    Scenario: Problem with current cost connexion with RabbitMQ activated
        When we start currentcost with bad port with rabbitmq
        Then we should see currentcost is unreachable in log
        And we should receive a message saying that current cost is unreachable

    Scenario: Current cost disconnected
        Given current cost does not send any message
        When we launch currentcost script and reach the timeout limit
        Then we should get informed that current cost does not send messages
        And we should see current cost does not send any message in log

    Scenario: Problem with USB port
        Given current cost is connected and currentcost script is launched
        When we disconnect USB port
        Then we should receive a message saying that current cost is disconnected
        And we should see currentcost is disconnected in log

    Scenario Outline: Problem with current cost message
        Given current cost is connected but send incorrect message
        When we launch currentcost script
        Then We should see this error in log

    Scenario Outline: Nominal case instant consumption
        Given current cost is connected
        When we launch currentcost script
        Then we should receive instant consumption over the network

    Scenario Outline: Nominal case historical consumption
        Given current cost is connected
        When we launch currentcost script
        Then we should receive historical consumption over the network
