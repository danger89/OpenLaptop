OpenLaptop Reverse SSH
======================

Reverse SSH is noodzakelijk om klanten te kunnen helpen ook als men achter een firewall of NAT zitten. In dit document wordt uitgelegd hoe dit tot stand wordt gebracht.

Client
------
1. Genereer een nieuwe SSH key pair (zonder private key wachtwoord): ```ssh-keygen -P "" -f ~/.ssh/id_openlaptop```
2. Download Public key van OpenLaptop Master Server en zet de key in de ~/.ssh/authorized_keys van de client
3. Zet de verbinding open en maak daarbij gebruik van de public key die net gegeneerd is bij stap 1: 
```ssh -R <random reverse port>:localhost:<client ssh port> serveruser@master.openlaptop.nl -i ~/.ssh/id_openlaptop.pub```

Server
------
1. Genereer SSH key met een sterk wachtwoord
2. Download de Public key van de client en zet de key in ~/.ssh/autorized_keys van de server
3. Maak verbinding naar de client:
```ssh -p <random reverse port> clientuser@localhost```
