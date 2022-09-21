#import
from genericpath import exists
from telnetlib import VT3270REGIME
from io import BytesIO
from tempfile import tempdir
import pandas as pd
import webbrowser, time 
import requests
import isodate
import time
import os
import gspread
import urllib.parse as urlparse


#Read the spreadsheet
def readSheet():
    spreadsheetId = "1glco8PeP_JmvgcEdDmDqeqHXVXQhCyqV53Dn5RPPhvE"
    url = "https://docs.google.com/spreadsheets/export?exportFormat=xlsx&id=" + spreadsheetId
    res = requests.get(url)
    data = BytesIO(res.content)
    List = pd.read_excel(data, sheet_name='test')
    Backup = pd.read_excel(data, sheet_name='List backup')
    return List, Backup

#get the time of video youtube
def getDuration(video_id):
    API_KEY = 'AIzaSyBj3flosOnOYncUolreFO5aeTMNfeurdzQ'
    respone = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id}&key={API_KEY}')
    data = respone.json()
    if not data.get('items'):
        return -1 #url not exist or still exist but video cleared/hidden from youtube
    else:
        toki = data['items'][0]['contentDetails']['duration']
        duration = isodate.parse_duration(toki).total_seconds()
    return duration

#is youtube url ?
def isYoutubeLink(link_in_sheet):
    if (("watch?v=" in link_in_sheet) or ("youtu.be" in link_in_sheet)):
        return True
    else:
        return False

#classify yoututbe url
def classifyYoutubeLink(link_youtube):
    if ("watch?v=" in link_youtube):
        return 0
    else:
        return 1

#check remain available link. Is youtube link still can play?
def countAvailableLink(video_id, listSong):
    client = gspread.service_account(filename="cool-plasma-362004-5043b3ab9bf9.json")
    sh = client.open("List music") # This is file's name not a sheet name
    wkslist = sh.worksheet("Copy List music")
    linkytb = listSong.Music.to_string(index=False).split()
    count = 0
    for i in range(len(linkytb)):
        if  isYoutubeLink(linkytb[i]) is True:
            if getDuration(video_id) == -1:
                count = count
            else:
                count += 1
        else:
            wkslist.delete_rows(i+1)
    return count

#check if need backup music or not
def needBackUp(video_id, listSong):
    if countAvailableLink(video_id, listSong) == 0:
        return 2
    if countAvailableLink(video_id, listSong) == 1:
        return 1 
    if countAvailableLink(video_id, listSong) >= 2:
        return 0

#get ID of all available link
def getIdFromLink(link_youtube):
    # linkytb = listSong.Music.to_string(index=False).split()
    if classifyYoutubeLink(link_youtube) == 1:
        url_data = urlparse.urlparse(link_youtube)
        query = urlparse.parse_qs(url_data.query)
        video_id = query["v"][0]
    else:
        video_id = link_youtube[-11:]
    return video_id

#add 2 music to array (music can be from list or backup)
def getTwoSongAvailable(listSong):
    linkytb = listSong.Music.to_string(index=False).split()
    two_song_info = []
    if needBackUp == 2:
        two_song_info.append(getIdFromLink(readSheet()[1][0]))#them 2 bai tu backup list vao mang
        two_song_info.append(getIdFromLink(readSheet()[1][1]))
    if needBackUp == 1:
        two_song_info.append(getIdFromLink(linkytb[0][0])) #them bai duy nhat trong list vao mang
        two_song_info.append(getIdFromLink(readSheet()[1][0])) #them 1 bai tu backup list vao mang
    if needBackUp == 0:
        two_song_info.append(getIdFromLink(linkytb[0][0])) #them 2 bai tu trong list vao mang
        two_song_info.append(getIdFromLink(linkytb[0][1]))
    return two_song_info

# run 2 song in array
def runTwoSong():
    two_song_in_list = getTwoSongAvailable(readSheet()[0])
    for i in range (len(two_song_in_list)):
        webbrowser.open(f"https://www.youtube.com/watch?v={two_song_in_list[i]}")
        time.sleep(getDuration(getIdFromLink(two_song_in_list[i])) + 9)
        os.system("killall -9 'Google Chrome'")
    return 
    

#run program
runTwoSong()
