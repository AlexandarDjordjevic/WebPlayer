#!/bin/python

import vlc
import logging
import threading
import time
from flask import Flask, render_template
import json
import os
from bluetooth import *

app = Flask(__name__)
btooth=Bluetoothctl()
p=vlc.MediaPlayer()
player_state = 0

def thread_function(name):   
    while True:
        global player_state
        print("State: " + str(player_state))
        if player_state == 0: #idle
            time.sleep(1)
        if player_state == 1: #start playing
            print("Playing stream")
            p.set_media("http://icy-5.radioparadise.com/mp3-128")
            p.play()
            player_state = 0
            time.sleep(5)
        if player_state == 2: #stop playing
            p.stop()
            player_state = 0
        

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_paired_devices")
def get_paired_devices():
    paired_list = btooth.get_paired_devices()
    return json.dumps(paired_list)

@app.route("/scan_available_devices")
def scan_available_devices():
    available_devices_list = btooth.start_scan()
    time.sleep(15)
    print(available_devices_list)
    return json.dumps(available_devices_list)

@app.route("/play_music")
def play_music():
    print ("Starting playback!")
    global player_state 
    player_state = 1
    return "0"

@app.route("/bluetooth_connect")
def bluetooth_connect():
    print ("Connecting to bluetooth speaker")
    btooth.connect("00:18:09:6A:2A:D5")
    return "0"

if __name__ == "__main__":
    x = threading.Thread(target=thread_function, args=(1,))
    x.start()
    app.run(host="0.0.0.0", debug=True)