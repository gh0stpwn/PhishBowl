import requests
import sys
import time
import datetime
import json
import datetime
import telepot
import urllib2
import csv

def urlscanner( urlstr ):
    headers = {
        'Content-Type': 'application/json',
        'API-Key': '8ff361ec-71f0-4aac-bfef-cb985134140a',
    }
    response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers,
        json={"url":urlstr, "public":"off"})
    json_out2 = response.json()
    time.sleep(2)
    return json_out2['uuid']

def notify(uuidtxt, urlstr):
    urlsan = urlstr.replace(":","[:]").replace(".","[.]").replace("http","hxxp").replace("-","[-]")
    time.sleep(250)
    response = requests.get('https://urlscan.io/api/v1/result/' + str(uuidtxt))
    jsonout = response.json()
    if (jsonout['data']['requests'][0]['response']['response']['status']) == 200:
      base_screen = 'https://urlscan.io/screenshots/'
      url = ''.join([base_screen, uuidtxt,'.png'])
      base_results = 'Phishing Alert | '
      base_results2 = ' | https://urlscan.io/result/'
      url2 = ''.join([base_results, urlsan])
      url3 = ''.join([url2, base_results2])
      url4 = ''.join([url3, uuidtxt])
      bot = telepot.Bot('858410252:AAGxcefiBF3Pd5xloGfRkWrd6_Fbmhcqu8k')
      bot.sendPhoto('-1001414226860', url, url4)


todays_date = datetime.datetime.now().strftime("%d-%m-%y")
clientList = ['canada','/cibc','/nbc','/bmo','/bnc','/national','/CIBC','/NBC','/BMO','/National','/BNC']
#nonClientList = ['bankofamerica','wells','america','simplii']
csv_file = todays_date + ".csv"
#download file and remove double qoutes
phish_url = 'https://phishstats.info/phish_score.txt'
phish_file = requests.get(phish_url)

with open(csv_file, "wb") as code:
    code.write(phish_file.content.replace('"',''))
#remove fist 9 lines and re-build file with only today's phishing links
with open(csv_file,"r") as f:
    lines_10_through_end = f.readlines()[9:]
with open(csv_file, "w") as f:
    for line in lines_10_through_end:
        if todays_date in line:
            f.write(line)
#replace the name with your actual csv file name
filelink = open(csv_file)
csv_reader = csv.reader(filelink)
second_column = [] #empty list to store second column values
for line in csv_reader:
    second_column.append(line[2])
    urlstr = line[2]
    if any(word in urlstr for word in clientList):
        uuidtxt = urlscanner( urlstr )
        notify(uuidtxt, urlstr)
