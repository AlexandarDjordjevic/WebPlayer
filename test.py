import vlc
import threading
import time
import os
import json

class Player:
    def __init__(self):
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.media = 0
        self.state = 0
        self.play_status = "stop"
        self.playlist = ""
        self.url = ""
        self.station_name = ""
        self.current_track = ""
        self.volume = 50
        self.mute = False
        self.thread = threading.Thread(target=self.worker, args=())

    def worker(self):   
        while True:
            print("State: " + str(self.state))
            if self.state == 0: #idle
                if self.media:
                    print('Playing')
                    #self.media.parse()
                    if self.mute:
                        self.media_player.audio_set_volume(0)
                    else:
                        self.media_player.audio_set_volume(self.volume)
                    # self.media_player.play()
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
                else:
                    print("Media error")
                    print("URL " + self.url)
                time.sleep(1)

            elif self.state == 1: #start playing
                print("Starting playback...")
                self.media=self.instance.media_new(self.url)
                self.media.get_mrl()
                self.media_player.set_media(self.media)
                self.media_player.play()
                self.play_status="play"
                self.state = 0

            elif self.state == 2: #stop playing
                self.media_player.stop()
                self.state = 0
                self.play_status="stop"

    def play(self, url):
        self.state = 1
        print("Play URL: " + url)
        self.url = url

    def stop(self):
        self.state = 2

    def init_playlist(self):
        json_file = open('playlist.json')
        self.playlist = json.load(json_file)

player = Player()

if __name__ == "__main__":
    player.url = "http://streaming.karolina.rs/karolina.mp3";
    player.thread.start()
    player.play("http://streaming.karolina.rs/karolina.mp3")
    while True:
        time.sleep(1)