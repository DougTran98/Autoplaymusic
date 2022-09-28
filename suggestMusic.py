# -*- coding: utf-8 -*-

#When user input name of music, auto return suggest link of music on youtube.

from distutils.log import error
from sys import stdout
from turtle import clear
import unicodedata
import urllib.request
import re
import requests
import isodate
from lxml import etree

#get and rewrite input
key1 = input("\nInput the song or singer that make you better: ")
key = key1.replace(' ','')
song = str(key.encode('utf-8'))
song = song.replace('b\'', '')
song = song.replace('\'', '')
song = song.replace('\\x', '%')

#claim all video by input
html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={song}")
video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

#show list video on youtube by input but not show video longer than 7 minutes (420 seconds)
API_KEY = 'AIzaSyBj3flosOnOYncUolreFO5aeTMNfeurdzQ'
video_ids = [
                title for title in video_ids if 
                (isodate.parse_duration
                    (
                        requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={title}&key={API_KEY}')
                        .json()['items'][0]['contentDetails']['duration']
                    )
                .total_seconds() <= 420
                )
            ]

print (f"\n~~~~~~~~~~~~ List bài \"{key1}\" nè ~~~~~~~~~~~~\n")
for title_count in range (len(video_ids)):
    url = str("https://www.youtube.com/watch?v=" + video_ids[title_count])
    youtube = etree.HTML(urllib.request.urlopen(url).read())
    video_url = youtube.xpath("/html/head/title")
    song_title = video_url[0].text
    song_title = song_title.encode('latin1').decode('utf8')
    if title_count > 9:
        break
    else:
        if title_count < 9:
            print (f'{title_count+1} . {song_title}')
        else:
            print (f'{title_count+1}. {song_title}')

while True:
    selection = input("\nChoose the song by number from 1 - 10: ")
    if selection.isdigit() is True:
        if int(selection) >=1 and int(selection) <=10:
            print(f"\n Link diu túp nè: https://www.youtube.com/watch?v={video_ids[int(selection)-1]}\n")
            break
        else:
            print("Wrong number, please input number from 1 - 10")
            continue
    else:
        print("Wrong input, please input number")
        continue
