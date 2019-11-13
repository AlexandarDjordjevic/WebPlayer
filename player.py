#!/bin/python

import vlc
import threading
import time
from flask import Flask, render_template, request
import json
import os
from bluetooth import *

class Player:
    def __init__(self):
        self.instance = vlc.Instance()
        self.media = vlc.MediaPlayer()
        self.state = 0
        self.playlist = ""
        self.url = ""
        self.thread = threading.Thread(target=self.worker, args=())

    def worker(self):   
        while True:
            if self.state == 0: #idle
                time.sleep(1)
            elif self.state == 1: #start playing
                print("Playing stream")
                self.media.set_mrl(self.url)
                self.media.play()
                self.state = 0
            elif self.state == 2: #stop playing
                self.media.stop()
                print ("Stop player!")
                self.state = 0
    def play(self, url):
        self.state = 1
        self.url = url

    def stop(self):
        self.state = 2

    def init_playlist(self):
        json_file = open('playlist.json')
        self.playlist = json.load(json_file)

app = Flask(__name__)
#btooth=Bluetoothctl()
player = Player()

@app.route("/")
def home():
    player.init_playlist()
    return render_template("index.html", playlist=player.playlist["online_stream"])

@app.route("/get_paired_devices")
def get_paired_devices():
    # paired_list = btooth.get_paired_devices()
    # return json.dumps(paired_list)
    return "OK"

@app.route("/scan_available_devices")
def scan_available_devices():
    return "OK"
    # available_devices_list = btooth.start_scan()
    # time.sleep(15)
    # print(available_devices_list)
    # return json.dumps(available_devices_list)

@app.route("/play", methods=['GET'])
def play_music():
    url_id = request.args.get('id')
    for item in player.playlist["online_stream"]:
        print(str(item["id"]))
        if item["id"] == int(url_id):
            print("Playing " + item["name"] + " " + item["url"])
            player.play(item["url"])
            break
    return render_template("index.html", playlist=player.playlist["online_stream"]), 200

@app.route("/stop", methods=['POST'])
def stop_playing_music():
    player.stop()
    return render_template("index.html", playlist=player.playlist["online_stream"]), 200

@app.route("/get_playlist", methods=['GET'])
def get_playlist():
    return player.playlist, 200

@app.route("/bluetooth_connect")
def bluetooth_connect():
    print ("Connecting to bluetooth speaker")
    # btooth.connect("00:18:09:6A:2A:D5")
    return "OK"

if __name__ == "__main__":
    player.thread.start()
    player.init_playlist()
    app.run(host="0.0.0.0", port=1234, debug=True)