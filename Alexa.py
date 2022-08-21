import speech_recognition as sr
import pyttsx3
import webbrowser
import pywhatkit as pyw
from selenium import webdriver
r = sr.Recognizer()
#drive = webdriver.Edge("C:\\Users\\Kaan\\Desktop\\msedgedriver.exe")
#drive.get("https://www.google.com/search?q=")
def repeat():

        with sr.Microphone() as source:
           audio = r.listen(source)
           voice = r.recognize_google(audio)
           if "nothing" in voice:
               pyttsx3.speak("Allright")
               exit()

           return voice

def main(voice):

    if "search" in voice:
        pyttsx3.speak("What do you want to search for?")
        objecttive = repeat()
        link = "https://google.com/search?q=" + objecttive
        webbrowser.get().open(link)
        pyttsx3.speak("Here's what I found")
    if "exit" in voice:
        pyttsx3.speak("See you")
        exit()
    if "play" in voice:
        voice = voice.replace("play", "")
        pyw.playonyt(voice)


pyttsx3.speak("Listening")
#while True:
try:
     if "Alexa" in repeat():

            pyttsx3.speak("Hello there, what can I do for you?")
            while True:
             main(voice=repeat())
except sr.UnknownValueError:
        pyttsx3.speak("sorry,I did not get that")









