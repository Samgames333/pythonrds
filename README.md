# pythonrds
A relatively simple python script to remotely change rt and ps text values for PiFmAdv.

This script will play audio on your desktop for a software like stereotool to then stream to the pi. This script will ssh the pi to change values in the control pipe. If you wish to use this on the pi with no outside computer, just modify the code to remove the ssh stuff. Then you can use stereotool or something else on the pi to stream the audio to PiFmAdv.

To run, you need the following python modules (some of which are included in python by default) and python 3.10.0 is recommended (that is the version I wrote this in):

json
random
paramiko
time
pygame
os

To install these, you can simply run ```pip install <module_name>```

To add more music, just put songs in the same folder as main.py (or a subfolder with a simple modification of line 12). For the script to recognize the songs, you will need to continue the format of the json file, which is pretty self-explanatory.
This script randomly shuffles the songs in the json. To turn this off you can edit the portion of the code to count up instead of generate a random number sequence to the amount of songs in the json. Note: the music files must be usable by pygame, meaning they must be a wav, mp3, or ogg file (subject to change). To route the audio output to stereotool you can use virtual audio cable or something similar, and I think using your desktop audio would work as well if you could figure out how to loop it back into stereotool or the software of your choice.

You may need to tweak this for it to work for your needs. I use stereotool to process and stream the audio this plays while this changes the RDS PS and RT values to diplay song names. NOTE: I may fix this in the future when I have time, but for now you will have to make sure the song name in the json file does not have words that are more than 8 characters long. If it does have those, just manually seperate them. The program goes by spaces between words so you could theoretically make scrolling ps text and add a seperate part to the json for the 64 character radio text.

I personally use a command along the lines of the following one on the pi to actually transmit everything:
```sox -v 1 -t mp3 http://X.X.X.X:PORT -c 2 -t wav -  | sudo ./pi_fm_adv --freq XXX --audio - --pi XXXX --ps "" --rt "" --pty X --preemph us --mpx 60 --ctl rds_ctl --ppm XX```

-v in sox changes the volume of the audio, default is 1. the X.X.X.X:PORT is where you would put localhost or your main desktop's ip and the port stereotool or other is streaming on. -c changes the number of channels. I have found that setting it to one will result in a cleaner and more efficient modulation, but there is not much of a difference so I prefer to stay with stereo. I would advise you to make a custom EQ in stereotool to prevent overmodulation past the normal 200khz of bandwidth because of loud high frequencies. You may need to use parameter --mpx with at least 50 if you want a normal audio transmit volume.
