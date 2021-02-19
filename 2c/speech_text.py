
import speech_recognition as sr

recognizer = sr.Recognizer()

need_love_audio = sr.AudioFile('audio/need_love.wav')

with need_love_audio as a:
    audio = recognizer.record(a)

text = recognizer.recognize_google(audio)

print(text)
