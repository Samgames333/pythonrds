#import the necessary modules for the code
import json
import random
import paramiko
import time
import pygame
import os

os.chdir(os.path.dirname(__file__))

#get the json file for later use
with open('music.json', 'r') as temp1:
    music = json.load(temp1)

#define variables to start
tempNum = 1
true = 1
jsonLength = 0
cycle = 1

#define variables and others for ssh connect later on
hostname = '192.168.X.X' #put your pi's lan ip (or the ip of the network your pi is connected to if you are away) here
port = 22 #the default port for the pi is 22, but change this if applicable
username = 'pi' #replace with your pi's username
password = 'raspberry' #replace with your pi's password
ssh = (paramiko.SSHClient())
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#get length of json in terms of songs as "jsonLength"
while true == 1:
    musicNum = str(tempNum)
    try:
        (music[musicNum][0])
    except:
        break
    tempNum = (tempNum + 1)
    jsonLength = (jsonLength + 1)

jsonLength = (jsonLength + 1)
tempCurrentSong = random.sample(range(1, jsonLength), (jsonLength - 1))
songChange = 0
while true == 1:
    #defines what song it will play
    currentSong = str(tempCurrentSong[songChange])

    pygame.mixer.init()
    pygame.mixer.music.load(music[currentSong][0]['filename'])
    pygame.mixer.music.play()

    #set the radiotext variable that will be used in rds_ctl in the form of both PS and RT
    RT = (music[currentSong][0]['musicname'])

    #connect to the Raspberry Pi
    ssh.connect(hostname, port, username, password)
    channel = (ssh.invoke_shell())

    #set RT (RadioText) value in the CTL file that is used when the Pi is transmitting
    channel.send('cd PiFmAdv/src\n')
    time.sleep(2)
    channel.send('cat >rds_ctl\n')
    time.sleep(1)
    channel.send('RT ' + RT + '\n')

    #detect if the length of RT is over 8 (which makes it incompatible with PS Text), then set PS to the individual words of RT, switching words every 2.5 seconds, if condition is true.
    if len(RT) >= 8:
        cycle = 1
        while true == 1:
            rtSplit = (RT.split())
            wordCount = len(rtSplit)
            time.sleep(2.5)
            channel.send('PS ' + rtSplit[cycle - 1] + '\n')
            cycle = cycle + 1
            if cycle >= (wordCount + 1):
                cycle = 1
            #detect if song ends, break while loop if when it does
            if pygame.mixer.music.get_busy() == False:
                break
    #this usually never happens if you add something like, for example, "on Samiack FM" to the end of the song name in the json file, but in case it does...
    else:
        channel.send('PS ' + RT + '\n')
        time.sleep(1)
    ssh.close()
    
    #play different songs from the json file list, error preventing function that resets song back to song 1 in the randomly generated order of songs from the list. This enables the script to hypothetically run 24/7 without manual control
    songChange += 1
    if songChange >= len(tempCurrentSong):
        songChange = 0