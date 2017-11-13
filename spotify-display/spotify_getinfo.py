#!/usr/bin/python

import os

def perfect_length(str):
	if len(str) > 23:
		return str[:21] + '...'
	else:
		return str

playing_song = os.popen("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:org.mpris.MediaPlayer2.Player string:Metadata | sed -n \'/title/{n;p}\' | cut -d \'\"\' -f 2|tr -d '\n'").read()
playing_artist = os.popen("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:org.mpris.MediaPlayer2.Player string:Metadata | sed -n \'/artist/{n;n;p}\' | cut -d \'\"\' -f 2|tr -d '\n'").read()
playing_album = os.popen("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:org.mpris.MediaPlayer2.Player string:Metadata | sed -n \'/album\"/{n;p}\' | cut -d \'\"\' -f 2| cut -d' ' -f-6 | tr -d '\n'").read()
artworkUrl= os.popen("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:org.mpris.MediaPlayer2.Player string:Metadata | sed -n \'/artUrl/{n;p}\' | cut -d \'\"\' -f 2|tr -d '\n'").read()
print(perfect_length(playing_song) + "\n${goto 40}" + perfect_length(playing_artist))

fstored_album = open(os.getenv('HOME') + '/.conky/spotify-display/stored_album.txt', 'r')
stored_album = fstored_album.readline().strip('\n')
fstored_album.close()

if playing_album != stored_album:
	# New cover needs to be downloaded
	os.system("wget -O $HOME/.conky/spotify-display/latest.jpg https://i.scdn.co/image/" + artworkUrl[31:])
	# If you'd like download a cover 174x174 instead of 64x64 use this one instead:no
	# os.system("wget -O $HOME/.conky/spotify-display/latest.jpg \"http://interactiveplaylist.com/ipfal?album=" + playing_album + "&artist=" + playing_artist + "\"")

	# Update current_song.txt using bash
	os.system("echo \"" + playing_album + "\" > $HOME/.conky/spotify-display/stored_album.txt")

