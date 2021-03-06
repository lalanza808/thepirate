#!/usr/bin/env python

"""
This Python script auto-adds new torrents from Pushbullet pushes if string starts with magnet:?
and combs through transmission downloads to remove torrents when 100% fully downloaded. Great for keeping my
ISP off my back. Sends Pushbullet notes on torrent removal

Add the location to your path and run it as a cron job on the same server as transmission and let it do it's thing

*/5 * * * * /opt/pirate/thepirate-satellite

Learn more about PushBullet here:
pushbullet.com
"""

__author__ = 'lance - github.com/lalanza808'


import transmissionrpc
import pushbullet
import requests
from time import sleep
from os import path,system

# Put your Pushbullet API key here
api = 'xxxxxxxxxx'

# Get rid of the SSL warnings
requests.packages.urllib3.disable_warnings()

##################################################
# Connect to transmission

t = transmissionrpc.Client('localhost', port=9091)
pb = pushbullet.Pushbullet(api)

# Remove completed torrents
for torrent in t.get_torrents():
	if torrent.percentDone == 1:
		print "[+] Removing torrent:\t{}".format(torrent.name)
		pb.push_note("Torrent Complete", torrent.name)
		sleep(3)
		t.remove_torrent(torrent.id)	
		
# Add new torrents
pushes = pb.get_pushes()
for push in pushes[1]:
	if push['body'].startswith('magnet:?'):
		system('/opt/pirate/thepirate-satellite.py --file {}'.format(str(push['body'])))
		pb.delete_push(push['iden'])
		
