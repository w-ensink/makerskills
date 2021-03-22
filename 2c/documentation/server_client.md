# Server <---> 2x Client

Omdat we in dit project een online game willen maken, waarbij je met 2 personen een spelletje kunt spelen, 
is het nodig om computers met elkaar te laten communiceren.
Als mediator wordt een server gebruikt. De server houdt de algehele staat
van het spel bij. De spelers spelen op een client. De client is verantwoordelijk voor het 
ontvangen van de user input, het sturen van vragen en antwoorden naar de server
en het weergeven van de game state aan de gebruiker.
De twee clients communiceren nooit direct met elkaar. De server is een soort mediator die ook delen 
van de logica van het spel beheert.

### Vooronderzoek
We wisten toen we begonnen nog niet zoveel van netwerk programmeren. 
Na enig basis onderzoek kwamen we erachter dat we het best iets met sockets konden gaan proberen. 
We kwamen erachter dat er twee soorten protocollen zijn hierbij; namelijk TCP en UDP. 
UDP is eenrichtings verkeer, waarbij de zender niet checkt of het bericht ontvangen is. Bij TCP is dit anders,
het check wel of het bericht daadwerkelijk is aangekomen. 
UDP is handig voor toepassingen die snel moeten werken en waarbij het niet heel erg uitmaakt of een bericht een keer wordt
gemist. 
Voor ons doeleinde is het wel belangrijk dat elk bericht aankomt en ook weer beantwoord wordt door de andere kant van de lijn.


Voorafgaand aan het programmeren hebben we wat onderzoek gedaan naar het programmeren met sockets in Python.
Wat ons het meest heeft geholpen is [deze Youtube video](https://www.youtube.com/watch?v=3QiPPX-KeSc).

### Voorinstallatie
Om dit stappenplan te kunnen volgen, heb je Python3 nodig. De sockets module die we gebruiken, wordt meegeleverd in de 
standard library van Python, dus deze hoeft niet los geinstalleerd te worden. 

### Eerste test
Als eerste test hebben we een simpele connectie gemaakt tussen 1 server en 1 client.
Dit hebben we gedaan met code van [techwithtim.net](https://www.techwithtim.net/tutorials/socket-programming/)

De client code ziet er zo uit:
```python
import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.26"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send("Hello World!")
input()
send("Hello Everyone!")
input()
send("Hello Tim!")

send(DISCONNECT_MESSAGE)
```

De server code ziet er zo uit:
```python
import socket 
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
```