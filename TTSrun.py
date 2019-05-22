import win32com.client as wincl
import os
path = os.path.dirname(os.path.abspath(__file__))
speak = wincl.Dispatch("SAPI.SpVoice")
print "hello"
while True:
    f = open("TTS.txt","r+")
    text = f.read()
    f.close
    if text != "":
        
        print("Message read")
        print(text)
        f = open("TTS.txt","w+")
        #f.write("")
        f.close
    text = text.replace("!tts","")
    speak.Speak(text)
