#!/bin/python
import time
from flask import Flask, render_template, request
import json
import os
from player import *
from stream import StreamList


app = Flask(__name__)
#btooth=Bluetoothctl()
player = Player()

@app.route("/")
def home():
    return render_template("index.html")

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

@app.route("/add_stream", methods=['POST'])
def add_stream():
    content = request.get_json();
    if content != None:
        StreamList.add_stream(content['name'], content['url'], content['genre'])
        return {"result" : "success"}, 200
    else:
        return {"result" : "error"}, 200

@app.route("/play", methods=['POST'])
def play():
    content = request.get_json();
    if content != None: 
        print(content)
        player.play(content['url'])
    else:
        player.play(player.url)
    return {"result" : "success"}, 200

@app.route("/stop", methods=['POST'])
def stop_music():
    player.stop()
    return {"result" : "success"}, 200

@app.route("/get_playlist", methods=['GET'])
def get_playlist():
    print("Get playlist!")
    return StreamList.get_list(), 200

@app.route("/bluetooth_connect")
def bluetooth_connect():
    print ("Connecting to bluetooth speaker")
    # btooth.connect("00:18:09:6A:2A:D5")
    return "OK"

@app.route("/current_playing")
def current_playing():
    return '{"status" : "'+ player.play_status +'", "station_name" : "'+ player.station_name + '", "current_track" : "' + player.current_track + '"}', 200

@app.route("/set_volume", methods=['POST'])
def set_volume():
    content = request.get_json();
    player.volume = int(content['volume']);
    player.mute = bool(content['mute']);
    return {"result" : "success"}, 200

if __name__ == "__main__":
    player.thread.start()
    app.run(host="0.0.0.0", port=1234, debug=True)
    