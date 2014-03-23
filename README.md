Functionnal test with fixtures to simulate CurrentCost on port COM and waited for currentCost to send messages.

## Development process:
 
 * Take a paper and write what you code should do and how it sould do that
 * Take a minute and update documentation
 * Then define a clear release roadmap 
 * Update README.md, CHANGELOG.txt, TODO.md
 * Add functional test
 * Add unit test while you don't pass functional test
 * Develop function has you don't pass unit test
 * Commit after each new implemented function
 * Create a release after each validation of functional test

## Workflow

    * N1: Start service
        * E1: Le service ne se lance pas. Envoi d'un message d'erreur sur le réseau et enregistrement de l'erreur dans un fichier de log.
    * N2: Arguments analysis
        * E2: Missing argument. Return an error and log it
        * E3: Bad value for an argument. Return and error and log it
    * N3: Connexion to current cost
        * E4: Unable to connect to current cost. Log error and return to step N3.
    * N4: 