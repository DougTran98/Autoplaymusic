from genericpath import exists
from telnetlib import VT3270REGIME
from io import BytesIO
import openpyxl
import pandas as pd
import webbrowser, time 
import requests
import isodate
import time
import os
import gspread
import urllib.parse as urlparse


#Read the spreadsheet
spreadsheetId = "1glco8PeP_JmvgcEdDmDqeqHXVXQhCyqV53Dn5RPPhvE"
url = "https://docs.google.com/spreadsheets/export?exportFormat=xlsx&id=" + spreadsheetId
res = requests.get(url)
data = BytesIO(res.content)
xlsx = openpyxl.load_workbook(filename=data)
List = pd.read_excel(data, sheet_name='List music')
History = pd.read_excel(data, sheet_name='History')

API_KEY = 'AIzaSyBj3flosOnOYncUolreFO5aeTMNfeurdzQ'

def getDuration (video_id):
    respone = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id}&key={API_KEY}')
    data = respone.json()
    if not data.get('items'):
        return -1
    else:
        toki = data['items'][0]['contentDetails']['duration']
        duration = isodate.parse_duration(toki).total_seconds()
        return duration

#check and claim right data and put data of two song into array
def getTwoSongAvailable (List):
    linkytb = List.Music.to_string(index=False).split()
    id_and_duration1 = []
    id_and_duration2 = []
    two_song_info = []
    for temp in range (len(linkytb)):
        if ("watch?v=" in linkytb[temp]) is True:
            url_data = urlparse.urlparse(linkytb[temp])
            query = urlparse.parse_qs(url_data.query)
            video_id = query["v"][0]
            if getDuration(video_id) == -1:
                temp += 1
            else:
                id_and_duration1.append(video_id)
                id_and_duration1.append(getDuration(video_id))
                two_song_info.append(id_and_duration1)
                if len(two_song_info) == 2:
                    break
                else: temp += 1
            # continue
        elif ("youtu.be" in linkytb[temp]) is True:
            video_id = linkytb[temp][-11:]
            if getDuration(video_id) == -1:
                temp += 1
            else:
                id_and_duration2.append(video_id)
                id_and_duration2.append(getDuration(video_id))
                two_song_info.append(id_and_duration2)
                if len(two_song_info) == 2:
                    break
                else: temp += 1
                # continue
        else:
            temp += 1
            # continue
    return (two_song_info)
print(getTwoSongAvailable(List))

#run 2 top of list
# webbrowser.open(linkytb[0])
# time.sleep(duration1 + 7)
# os.system("killall -9 'Google Chrome'")
# webbrowser.open(linkytb[1])
# time.sleep(duration2 + 13)
# os.system("killall -9 'Google Chrome'")

# #move 2 top of list to [History] after play music
# client = gspread.service_account(filename="cool-plasma-362004-5043b3ab9bf9.json")
# sh = client.open("List music")
# wkslist = sh.worksheet("List")
# wkshistory = sh.worksheet("History")

# remove = wkslist.get('A2:C3')

# wkshistory.append_rows(remove)

# wkslist.delete_rows(2)
# wkslist.delete_rows(2)

