#!/usr/bin/env python

import argparse
import random
import mpd
from socket import error as SocketError

HOST = 'localhost'
PORT = '6600'

class Client(object):
    def __init__(self, host, port, args):
        self.args = args

        self.mpd = mpd.MPDClient()
        self.host = host
        self.port = port
        self.connect()

        if self.args.loop:
            self.wait_for_end()
        else: 
            self.process()


    def connect(self):
        try:
            self.mpd.connect(self.host, self.port)
        except SocketError:
            print("failed to connect to mpd")
            exit(1)

    def clear(self):
        self.mpd.clear()

    def process(self):
        if self.args.clear:
            self.clear()

        self.artist = self.args.artist

        if self.args.confirm:
            self.album = self.confirmLoop()
        else:
            self.album = self.getAlbum(self.artist)

        self.add()

    def getAlbum(self, artist=None):
        #import pdb; pdb.set_trace()
        if artist is not None:
            try:
                album = random.choice(self.mpd.list('Album', 'artist', self.artist))
            except:
                print "Error: artist {} is not in the library".format(self.artist)
                exit(1)
        else:
            album = random.choice(self.mpd.list('Album'))

        return album
    
    def getArtist(self):
        return self.artist or self.mpd.list('artist', 'album', self.album)[0]

    def confirmLoop(self):
        while True:
            self.album = self.getAlbum(self.artist)
            art = self.artist or self.mpd.list('artist', 'album', self.album)[0]
            print "{} - {}".format(art, self.album)
            answer = raw_input("Add this album (y/n): ")
            if answer == "y":
                return self.album

    def wait_for_end(self):
        while True:
            if self.mpd.status().get('state') == 'stop':
                self.process()
                self.mpd.play()
            self.mpd.idle()


    def add(self):
        files = self.mpd.list('filename', 'album', self.album)
        if not args.test:
            for f in files:
                self.mpd.add(f)
        print("added {} - {}".format(self.album, self.getArtist()))
    
    def disconnect(self):
        self.mpd.disconnect()

        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add random album to the queue')

    parser.add_argument(
            "-rm", "--clear",
            dest="clear",
            action='store_true',
            help="Replace the current queue instead of appending",
            )

    parser.add_argument(
            "-c", "--confirm",
            dest="confirm",
            action='store_true',
            help="Confirm album selection before adding",
            )

    parser.add_argument(
            "-a", "--artist",
            dest="artist",
            help="Limit album choice to specific artist",
            )

    parser.add_argument(
            "-l", "--loop",
            dest="loop",
            action='store_true',
            help="Auto add album when playback finishes",
            )

    parser.add_argument(
            "-t", "--test",
            dest="test",
            action='store_true',
            help="Do a test run without adding"
            )

    args = parser.parse_args()
    client = Client(HOST, PORT, args)
    client.disconnect()
