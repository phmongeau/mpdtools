# This is a collection of scripts I use with the Music Player Deamon (mpd)

## randAlbum.py

	usage: randAlbum.py [-h] [-rm] [-c] [-a ARTIST] [-l] [-t]

	Add random album to the queue

	optional arguments:
	  -h, --help            show this help message and exit
	  -rm, --clear          Replace the current queue instead of appending
	  -c, --confirm         Confirm album selection before adding
	  -a ARTIST, --artist ARTIST
							Limit album choice to specific artist
	  -l, --loop            Auto add album when playback finishes
	  -t, --test            Do a test run without adding
