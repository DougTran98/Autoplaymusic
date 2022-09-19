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

#Read the spreadsheet
spreadsheetId = "1glco8PeP_JmvgcEdDmDqeqHXVXQhCyqV53Dn5RPPhvE"
url = "https://docs.google.com/spreadsheets/export?exportFormat=xlsx&id=" + spreadsheetId
res = requests.get(url)
data = BytesIO(res.content)
xlsx = openpyxl.load_workbook(filename=data)
List = pd.read_excel(data, sheet_name='List music')
History = pd.read_excel(data, sheet_name='History')

#put data on sheet to array
linkytb = List.Music.to_string(index=False).split()

#get the time of youtube's link
video_id1 = linkytb[0][-11:]
video_id2 = linkytb[1][-11:]
API_KEY = 'AIzaSyBj3flosOnOYncUolreFO5aeTMNfeurdzQ'
respone1 = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id1}&key={API_KEY}')
respone2 = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id2}&key={API_KEY}')
data1 = respone1.json()
data2 = respone2.json()
toki1 = data1['items'][0]['contentDetails']['duration'] #case link lỗi, case data trống,
toki2 = data2['items'][0]['contentDetails']['duration']
duration1 = isodate.parse_duration(toki1).total_seconds()
duration2 = isodate.parse_duration(toki2).total_seconds()

#run 2 top of list
webbrowser.open(linkytb[0])
time.sleep(duration1 + 7)
os.system("killall -9 'Google Chrome'")
webbrowser.open(linkytb[1])
time.sleep(duration2 + 13)
os.system("killall -9 'Google Chrome'")

#move 2 top of list to [History] after play music
# client = gspread.service_account(filename="cool-plasma-362004-5043b3ab9bf9.json")
# sh = client.open("List music")
# wkslist = sh.worksheet("List")
# wkshistory = sh.worksheet("History")

# remove = wkslist.get('A2:C3')

# wkshistory.append_rows(remove)

# wkslist.delete_rows(2)
# wkslist.delete_rows(2)

