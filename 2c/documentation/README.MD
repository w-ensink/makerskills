
# Documentation

---

### Server <---> 2x Client
Omdat we in dit project een online game willen maken, waarbij je met 2 personen een spelletje kunt spelen, 
is het nodig om computers met elkaar te laten communiceren.
Als mediator wordt een server gebruikt. De server houdt de algehele staat
van het spel bij. De spelers spelen op een client. De client is verantwoordelijk voor het 
ontvangen van de user input en het weergeven van de game state aan de gebruiker.
De twee clients communiceren nooit direct met elkaar.

---

### Protocol
Om data over TCP te sturen, hebben we een protocol nodig.
Dit protocol zorgt ervoor dat beide zijden (server & client) elkaar begrijpen.
Beide spreken als het ware dezelfde taal als het gaat om berichten en afbeeldingen.

De soorten data die ons protocol moet kunnen afhandelen, zijn:
* Afbeeldingen
* Tekstberichten
* Integer waarden

Van deze data typen moet het protocol binary data kunnen maken en het moet ook 
kunnen vertellen wat voor data het is als je de binary aan het protocol geeft.

---

### Demo

https://www.youtube.com/watch?v=Iol8jyYqFBU

Eerste demo waarin de werking van de client/server communicatie zichtbaar (en hoorbaar) is.
Deze demo is gefilmd vanuit Wouter zijn perspectief, spelend tegen Paul. Paul is ook op de achtergrond te horen.