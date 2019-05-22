import win32com.client as wincl
import os
path = os.path.dirname(os.path.abspath(__file__))
speak = wincl.Dispatch("SAPI.SpVoice")


speak.Rate = 3 ## Rate of speech: -10 (slowest) to 10 (fastest)
speak.Volume = 100 ## Speech volume: 0 - 100

print "Keep this window open to allow Text to Speech"
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
    speak.Speak(text)
    
    
