# ChatTTS
A Streamlabs Chatbot script that allows a viewer to use TTS

This is an early version of the script. You need to run TTSrun.py manually (and keep the window open, but minimised) for the TTS to work.

Future versions will fix this.

If TTSrn.py crashes, it might be because win32com library is not installed. So, open Command Prompt, and type "start C:\python27\scripts\pip.exe install win32com" (without quotes) to install the library. Once it is installed, close command prompt and try TTSrun.py again. You will need to do this only once.

To change the rate and volume of speech: 
1- right click on TTSrun.py

2- Choose Edit with IDLE

3- adjust the values of speak.Rate and speak.Volume

4- Save, run the file, and close IDLE when you finish editing.


Errors are logged on a text file in the script folder, and will appear under 'information' in the script tab on Chatbot. If the script is not running, check the ErrorLog.txt file. If you could not solve the issue, delete the ErrorLog.txt file, run the script. If a new ErrorLog.txt file is created, contact me and attach the log file. 
