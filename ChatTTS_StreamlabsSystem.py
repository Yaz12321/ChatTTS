
#---------------------------------------
#    Import Libraries
#---------------------------------------

import clr, sys, json, os, codecs
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import time
import winsound
from ast import literal_eval
import random
import re
import datetime
from datetime import datetime, timedelta


#---------------------------------------
#    [Required]    Script Information
#---------------------------------------
# These are the script details that appear on the bot.
ScriptName = "ChatTTS"
Website = ""
Creator = "Yaz12321"
Version = "0.1"
Description = "Convert whispers to bot into speech"

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
#   Version Information
#---------------------------------------

# Version:

# > 0.1 <
    # Testing version

#---------------------------------------
#    Load and Define Settings
#---------------------------------------

class Settings:
    # Tries to load settings from file if given
    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile = None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig',mode='r') as f:
                        self.__dict__ = json.load(f, encoding='utf-8-sig')
        else: #set variables if no settings file
            self.OnlyLive = False
            self.TTSstart = "!ttsstart"
            self.TTSend = "!ttsend"
            self.TTStext = "!tts"
            self.Permission = "Caster"
            self.PermissionInfo = ""
            self.Cost = 0
            self.UseCD = False
            self.CoolDown = 0
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 0
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.NotEnoughResponse = "{0} you don't have enough points to run command"
            self.Payout = 0
            self.ttsSmsg = "{0}, you are now in control of TTS. Whisper: {1} followed by the messages. Please do not abuse!"
            self.ttsEmsg = "{0}, you can no longer control TTS. Thank you."


    # Reload settings on save through UI
    def ReloadSettings(self, data):
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        with codecs.open(settingsFile,  encoding='utf-8-sig',mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig',mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
        return


#---------------------------------------
# Initialize Data on Load
#---------------------------------------
def Init():
    # Any actions that should happen when the script is initialised should go here.
    # Define global variables here
    # Globals
    global MySettings

    # Load in saved settings
    MySettings = Settings(settingsFile)

    global TTS
    TTS = False

    global viewer
    viewer = "hello"

    # End of Init
    return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsonData):
    # Globals
    global MySettings

    # Reload saved settings
    MySettings.ReloadSettings(jsonData)

    # End of ReloadSettings
    return


#---------------------------------------
#    Functions
#---------------------------------------

# A collection of variables that can be useful while coding.

def path(): # Get path of file
    path = os.path.dirname(os.path.abspath(__file__))
    return path

def log(message): # Log errors in a text file for each script
    exc_type, exc_obj, exc_tb = sys.exc_info()
    line = exc_tb.tb_lineno
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    try:
        errorfile = open("{}/ErrorLog.txt".format(path()),"a+")
    except:
        errorfile = open("{}/ErrorLog.txt".format(path()),"w+")
    errortime = time.strftime("%d %b %Y %H:%M:%S", time.localtime())
    error = "[{}]: (File: {}) (Line: {}) {} \n".format(errortime,fname,line,message)
    errorfile.write(error)
    errorfile.close()
    error = "[{}]: (File: {}) (Line: {}) {}".format(errortime,fname,line,message)
    Parent.Log(ScriptName,error)
    return


def twitchmsg(message): # A shortcut to sending twitch message
    Parent.SendTwitchMessage(message)
    return

def whisper(user,message): # A shortcut to sending twitch whisper
    Parent.SendStreamWhisper(user,message)
    return


def Filtercharacters(string): # remove non-alphanurmeric characters from string (can be changed to numeric or others)
    filtered = re.sub('\W+',' ', string )
##   filtered = re.findall(r"[-+]?\d*\.\d+|\d+", i) ##for numbers only
##   \W+ get from: https://docs.python.org/2/library/re.html
    return filtered

def randi(mn,mx): # returns a random number based on system time
    r = time.time()*100
    if mx != mn:
        rand = r%(mx-mn) + mn
    else:
        rand = mx

    return int(rand)

def randl(): # returns a random letter of the alphabet (needs randi)
    r = randi(0,27)
    letters = "abcdefghijklmnopqrstuvwxyz"
    rl = letters[r]
    return rl

def PlaySound(soundfile): # Play the file soundfile.wav. Has to be in the same folder as script
    winsound.PlaySound(soundfile, winsound.SND_FILENAME|winsound.SND_ASYNC)
    return


def PlaySysSound(syssound): # Plays a system sound: ('SystemAsterisk','SystemExclamation','SystemExit','SystemHand','SystemQuestion')
    winsound.PlaySound(syssound, winsound.SND_ALIAS)
    return

def CheckLive(): # For scripts that have "OnlyLive" Setting, allows command to continue based on stream status.
    #check if command is in "live only mode"
    if MySettings.OnlyLive:

        #set run permission
        startCheck = Parent.IsLive()

    else: #set run permission
        startCheck = True
    return startCheck


def find_max_index(lst,Index): # Ind is bool: True: return random from list, False: retrun all list
    MaxCount = max(lst)
    Winners = [i for i, j in enumerate(lst) if j == MaxCount]
    n = Winners[Parent.GetRandom(0,len(Winners))]
    if Index:
        return n
    else:
        return Winners



def find_min_index(lst,Index): # Index is bool: True: return random from list, False: retrun all list
    MinCount = min(lst)
    Winners = [i for i, j in enumerate(lst) if j == MinCount]
    n = Winners[Parent.GetRandom(0,len(Winners))]
    if Index:
        return n
    else:
        return Winners

def Execute(data): # Handle chat messages. Function is called whenever there is a message in chat.
                    # data objects only work here.
    try: # In case of error, it will skip to except
        if data.IsChatMessage() and data.GetParam(0).lower() == MySettings.TTSstart and Parent.HasPermission(data.User, MySettings.Permission, MySettings.PermissionInfo):

            startCheck = CheckLive()
            global TTS
            TTS = True
##            path = os.path.dirname(os.path.abspath(__file__))
##            #os.system("start \"{}\TTSrun.py\"".format(path))
##            os.system("start {}\TTSrun.py".format(path))
            global viewer
            viewer = data.GetParam(1)
            whisper(viewer,MySettings.ttsSmsg.format(viewer,MySettings.TTStext))
            
        if data.IsChatMessage() and data.GetParam(0).lower() == MySettings.TTSend and Parent.HasPermission(data.User, MySettings.Permission, MySettings.PermissionInfo):
            startCheck = CheckLive()
            global TTS
            TTS = False
            whisper(viewer,MySettings.ttsEmsg.format(viewer))

        
        if MySettings.TTStext == "":
            TTST = True
        else:
            if data.GetParam(0).lower() == MySettings.TTStext:
                TTST = True
            else:
                TTST = False    

        #check if user has permission
        if data.IsChatMessage() and TTST and data.User.lower() == viewer.lower():
            path = os.path.dirname(os.path.abspath(__file__))
            text = data.Message
            text = text.replace(MySettings.TTStext,"")
            f= open("{}/TTS.txt".format(path),"w+")
            f.write(text)
            f.close
            


    except Exception as ex: # use log() function to log the error
        log(ex)
    return


#---------------------------------------
#    Bottom Functions
#---------------------------------------
def Tick(): # Runs whenever there is no data. Timers, and repeated actions go here
    
    return

def UpdateSettings():
    with open(m_ConfigFile) as ConfigFile:
        MySettings.__dict__ = json.load(ConfigFile)
