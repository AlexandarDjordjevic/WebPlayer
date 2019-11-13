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
        self.media_player = self.instance.media_player_new()
        self.media = 0
        self.state = 0
        self.playlist = ""
        self.url = ""
        self.station_name = ""
        self.current_track = ""
        self.thread = threading.Thread(target=self.worker, args=())

    def worker(self):   
        while True:
            if self.state == 0: #idle
                if self.media:
                    self.media.parse()
                    if self.media.get_meta(0):
                        self.station_name = self.media.get_meta(0)
                    else:
                        self.station_name = " "
                    if self.media.get_meta(12):
                        self.current_track = self.media.get_meta(12)
                    else:
                        self.current_track = " " 
                    print(self.station_name)
                    print(self.current_track)
                    # for i in range(13):
                    #     print("{} - {}".format(i, self.media.get_meta(i)))
                time.sleep(3)
            elif self.state == 1: #start playing
                print("Playing stream")
                self.media=self.instance.media_new(self.url)
                self.media.get_mrl()
                self.media_player.set_media(self.media)
                self.media_player.play()

                self.state = 0
            elif self.state == 2: #stop playing
                self.media_player.stop()
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

@app.route("/get_artist")
def get_artist():
    return '{"station_name" : "'+ player.station_name + '", "current_track" : "' + player.current_track + '"}', 200

if __name__ == "__main__":
    player.thread.start()
    player.init_playlist()
    app.run(host="0.0.0.0", port=1234, debug=True)