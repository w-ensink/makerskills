# Speech to Text

Voor ons project is het belangrijk dat we gebruikersinput via stem kunnen verkrijgen.
Het is de bedoeling dat de gebruiker iets in kan spreken, en dat dat wordt omgezet in tekst.
Deze tekst wordt dat doorgestuurd naar de server en daar geintepreteerd en doorgestuurd.

---
### Vooronderzoek
Van tevoren hebben we natuurlijk even uitgezocht of wat we wilden uberhaupt mogelijk is.
Al snel bleek dat het kon via de ```speechrecognition``` module in Python.
Op internet zijn enkele voorbeelden te vinden van hoe deze in de basis te gebruiken is.

### Voorinstallatie
Om dit stappenplan te kunnen doen zijn de volgende programma's en libraries vereist:
* Python3
* pip3

Vervolgens moeten een aantal libraries voor Python worden geinstalleerd met de volgende commando's:
```bash
pip3 install speechrecognition
pip3 install pyaudio
```

### Eerste test
Als eerste test, wilden we kijken of het mogelijk was om spraakherkenning op een bestaand audio bestand toe te passen.
Na enig online onderzoek, kwamen we op de volgende code:
```python3
import speech_recognition as sr

recognizer = sr.Recognizer()

audio_file = sr.AudioFile('audio/english_file.wav')

with audio_file as a:
    audio = recognizer.record(a)

text = recognizer.recognize_google(audio)

print(text)
```

Deze opent een audio recognizer en een audio bestand, 
neemt de audio vanuit het bestand op met de recognizer 
en stuurt dit vervolgens naar Google. Na even wachten krijgt het de tekst terug.
Deze wordt dan naar de console geprint.

Voor deze eerste test hebben we een engels audio bestand gepakt.

### Nu live inspreken
Nadat we een sample konden analyseren, was het tijd om hetzelfde werkend te krijgen 
met live audio. Na wederom enig zoekwerk vonden we een spelletje waarin dit voorkwam.
We hebben enkel het live audioherkenning gedeelte eruit geisoleerd en vertaald naar
een behapbare, functionele functie:
```python3
import speech_recognition as sr

def get_speech_input_as_text():
    microphone = sr.Microphone()
    recognizer = sr.Recognizer()
    
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.RequestError:
        return ''
    except sr.UnknownValueError:
        return ''
```
Als je deze functie aanroept, kun je je verhaal in het Engels inspreken,
waarna je (na even wachte) dit verhaal als tekst terugkrijgt.

De twee ```except``` blokken zijn voor als er een exception wordt geworpen door 
de recognizer. Dit kan voorkomen bij problemen met de internetverbinding 
(als ```sr.RequestError```) of als Google niks van de input kan maken 
(als ```sr.UnknownValueError```). Op dit moment geven beide een lege string terug.

### Nu in het Nederlands
Wij wilden graag dat ons spel speelbaar zou zijn in het Nederlands.
Na enig onderzoek online, bleek het super simpel te zijn om dat werkend te krijgen.
De functie ```recognize_google()``` bleek nog een extra (optioneel) argument te hebben.
De nieuwe versie van de functie hierboven die Nederlands begrijpt, ziet er dan zo uit:
```python3
import speech_recognition as sr

def get_speech_input_as_text():
    microphone = sr.Microphone()
    recognizer = sr.Recognizer()
    
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio, language='nl-NL')
    except sr.RequestError:
        return ''
    except sr.UnknownValueError:
        return ''
```

### Nu in een abstractie die bruikbaar is voor onze game

```python3
import speech_recognition as sr

class SpeechToText:
    def __init__(self):
        pass

    def get_user_input(self):
        microphone = sr.Microphone()
        recognizer = sr.Recognizer()
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.6)
            audio = recognizer.listen(source)

        try:
            response = recognizer.recognize_google(audio, language='nl-NL')
            return response
        except sr.RequestError:
            return self.get_user_input()
        except sr.UnknownValueError:
            return self.get_user_input()

    def get_user_confirmation(self):
        answer = self.get_user_input()
        while answer != 'ja' and answer != 'nee':
            answer = self.get_user_input()
        return answer == 'ja'
```
Wat opvalt, is dat we hebben gekozen voor twee verschillende soorten input.
Aan de ene kant willen we gewoon tekst als input hebben, waarbij de gebruiker exact bepaalt
wat hij wil zeggen. Aan de andere kant hebben we een functie die alleen 'ja' of 'nee' accepteert.
Dit doen we, omdat dit de twee belangrijkste doelen van de speech to text module binnen ons spel.
Verder valt op dat we bij problemen met het verstaan, telken opnieuw blijven proberen.