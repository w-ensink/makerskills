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

### Port forwarding
Om via internet connectie te maken met andere computers, moet je gebruik maken van port forwarding.
Je computer is standaard van de buitenwereld afgeschermd door je router.
Om toch je computer bereikbaar te maken, kun je port forwarding gebruiken. 
De buitenwereld (die niet is aangesloten op jouw router/wifinetwerk), kan enkel jouw router
bereiken via diens IP address. Dit IP address ziet er ongeveer zo uit: ```84.104.226.201``` 
waarbij de cijfers natuurlijk verschillen per router. 

Je server maakt verbinding met je router. 
In het lokale netwerk heeft je server dan een lokaal IP address.
Dit ziet er meestal ongeveer zo uit: ```192.168.178.10``` 
waarbij de cijfers achter laatste punt verschillen per apparaat in je netwerk.

Als je een TCP-verbinding maakt, gaat dat altijd via een bepaalde poort. In de instellingen van je router
kun je ervoor kiezen om bepaalde poorten door te verbinden met een lokaal IP address. 
Zo kun je bijvoorbeeld kiezen om poort ```5000``` van IP ```84.104.226.201``` 
door te sturen naar poort ```4000``` van het lokale IP ```192.168.178.10```.

Op deze manier kan een client buiten jouw lokale netwerk verbinding maken met poort ```5000``` en IP ```84.104.226.201```
en kun je deze client bedienen met je server met het lokale IP ```192.168.178.10``` op poort ```4000```.

---
### Eerste test: één client 
Deze code komt van [deze tutorial](https://realpython.com/python-sockets/).

Client:
```python
import socket
import time

HOST = '84.104.226.201'  # The server's hostname or IP address
PORT = 50_000  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        s.sendall(b'Hello, world')
        data = s.recv(1024)
        print('Received', repr(data))
        time.sleep(0.1)
```

Server:
```python
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 50_000        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
```

---
### Tweede test: meerdere clients
Als tweede test hebben we een simpele connectie gemaakt tussen 1 server en meerdere clients.
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
---
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
---
### Uiteindelijke abstracties
```python
class Protocol:
    def encode_text(self, text):
        binary = text.encode('utf-8')
        header = b'txt_'
        message = header + binary
        return message
    
    def get_format(self):
        return 'utf-8'

    def decode_text(self, binary):
        return str(binary)[4:]

    def is_encoded_text(self, binary):
        return binary[:4] == b'txt_'

    def get_header_size(self):
        return 64

    def encode_message_length_header(self, length):
        length = str(length).encode('utf-8')
        length += b' ' * (self.get_header_size() - len(length))
        return length
```


Voor je client hebben we de class ServerConnection gemaakt.
```python
import socket
import protocol

class ServerConnection:
    def __init__(self, address):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(address)
        self.protocol = protocol.Protocol()

    def close(self):
        self.client.close()

    def send_message(self, message):
        encoded_msg = self.protocol.encode_text(message)
        length = self.protocol.encode_message_length_header(len(encoded_msg))
        self.client.send(length)
        self.client.send(encoded_msg)

    def wait_for_message(self):
        length = self.client.recv(self.protocol.get_header_size()).decode(self.protocol.get_format())
        if length:
            length = int(length)
            message = self.client.recv(length).decode(self.protocol.get_format())
            message = self.protocol.decode_text(message)
            return message
```

Voor de server hebben we de ClientConnection gemaakt.

```python
import socket
import protocol

class ClientConnection:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.protocol = protocol.Protocol()

    def __del__(self):
        self.connection.close()

    def wait_for_message(self):
        length = self.connection.recv(self.protocol.get_header_size()).decode(self.protocol.get_format())
        if length:
            length = int(length)
            message = self.connection.recv(length).decode(self.protocol.get_format())
            message = self.protocol.decode_text(message)
            return message

    def send_message(self, message):
        message = self.protocol.encode_text(message)
        length = self.protocol.encode_message_length_header(len(message))
        self.connection.send(length)
        self.connection.send(message)

    def close(self):
        self.connection.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class Server:
    def __init__(self, ip_address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = socket.gethostbyname(ip_address)
        address = (server, port)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(address)
        self.client_connections = []

    def wait_for_num_client_connections(self, num):
        self.server.listen()
        while len(self.client_connections) < num:
            connection, address = self.server.accept()
            self.client_connections.append(ClientConnection(connection, address))
        return self.client_connections

    def close(self):
        for c in self.client_connections:
            c.close()
        self.server.close()
```