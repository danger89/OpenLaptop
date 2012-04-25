OpenLaptop Reverse SSH
======================

Het kan handig zijn om toegang te krijgen tot het systeem van de gebruiker in geval een ernstig probleem, om de klant van dienst te kunnen zijn, die achter een firewall of NAT zit, kan er gebruik worden gemaakt van Reverse SSH. In dit document wordt uitgelegd hoe dit tot stand kan worden gebracht.

Een alternative is TeamViewer.

Client
------
1. Genereer een nieuwe SSH key pair (zonder private key wachtwoord): ```ssh-keygen -P "" -f ~/.ssh/id_openlaptop```
2. Download Public key van OpenLaptop Master Server en zet de key in de ~/.ssh/authorized_keys van de client
3. Zet de verbinding open en maak daarbij gebruik van de public key die net gegeneerd is bij stap 1: 
```ssh -o 'StrictHostKeyChecking no' -R <random reverse port>:localhost:<client ssh port> serveruser@master.openlaptop.nl -i ~/.ssh/id_openlaptop```

Server
------
1. Genereer SSH key met een sterk wachtwoord
2. Download de Public key van de client en zet de key in ~/.ssh/autorized_keys van de server
3. Maak verbinding naar de client:
```ssh -p <random reverse port> clientuser@localhost```
