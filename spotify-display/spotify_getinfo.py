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

fle=os.popen("/usr/bin/gsettings get org.gnome.desktop.background picture-uri").read()
fle=fle.replace("\n", " ")
fstored_album = open(os.getenv('HOME') + '/.conky/spotify-display/stored_album.txt', 'r')
stored_album = fstored_album.readlines()
fstored_album.close()

if (playing_album+fle).strip('\n') != stored_album[0].strip('\n'):
	# New cover needs to be downloaded
	os.system("wget -O $HOME/.conky/spotify-display/latest.jpg https://i.scdn.co/image/" + artworkUrl[31:])
	# If you'd like download a cover 174x174 instead of 64x64 use this one instead:no
	# os.system("wget -O $HOME/.conky/spotify-display/latest.jpg \"http://interactiveplaylist.com/ipfal?album=" + playing_album + "&artist=" + playing_artist + "\"")
	#quailty code
	size=os.popen(("identify "+fle)).read().split(" ")[2].split("x")
	wall_height=int(size[0])
	wall_width=(wall_height/1920)*400
	avgColor=os.popen("convert "+fle+" -crop " + str(wall_width) + "x"+ str((int(size[1])/1080)*300) +"+"+str(wall_height-wall_width)+"+""15 -scale 1x1\\! txt:-").read()[1:].split("(")[2][:-2].split(",")
	if (float(avgColor[0])*0.299 + float(avgColor[1])*0.587 + float(avgColor[2])*0.114) > 186:
		colora=str(3)
		coloraa=str(2)
	else:
		colora=str(0)
		coloraa=str(1)
	# Update current_song.txt using bash 380*150
	os.system("echo \"" + ((playing_album + fle).strip('\n')+"\n"+colora+"\n"+coloraa) + "\" > $HOME/.conky/spotify-display/stored_album.txt")
	#1475
else:
	colora=str(stored_album[1]).strip("\n")
	coloraa=str(stored_album[2]).strip("\n")

print("${color"+colora+"}${font LL_Record:size=14}${goto 10}d${font}${color"+coloraa+"}${goto 40}${voffset -8}" + perfect_length(playing_song) + "\n${goto 40}" + perfect_length(playing_artist))
