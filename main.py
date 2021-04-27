'''
usage:
python3 main.py [city_name:NewTaipei] [route_name:藍23] [stop_name:捷運昆陽站] [direction:0]
'''
import sys
import json
import requests
from datetime import datetime
from requests.utils import quote
from posixpath import join as pjoin

import telebot


# init
city = sys.argv[1]
route_name = sys.argv[2]
stop_name = sys.argv[3]
direction = int(sys.argv[4])
ptx_url = "https://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/City"
headers = {
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
}
with open('secret.json', 'r') as f:
    secret = json.load(f)

token = secret['token']
chat_id = secret['chat_id']
bot = telebot.TeleBot(token)

# construct query_url
query = "{}?$filter=StopName/Zh_tw eq '{}'&$format=JSON".format(route_name, stop_name)
query = quote(query, safe="?$='&")
query_url = pjoin(ptx_url, city, query)

# query
api_data = requests.get(url=query_url, headers=headers).json()

for data in api_data:
    if data['Direction'] != direction:  # 只處理往昆陽捷運站
        continue
    if (data['EstimateTime'] / 60 > 12.0) or (data['EstimateTime'] / 60 < 3.0):  # 到站時間大於10分鐘/小於3分鐘不傳訊息
        continue

    update_time = datetime.strptime(data['UpdateTime'], '%Y-%m-%dT%H:%M:%S+08:00')
    # construct message
    message = "{}公車資訊\n".format(data['RouteName']['Zh_tw'])
    message += "{}\n".format(data['StopName']['Zh_tw'])
    message += "到站剩餘： {:.1f} 分鐘\n".format(data['EstimateTime'] / 60)
    message += "更新時間： {}\n".format(update_time.strftime('%H:%M'))

    bot.send_message(chat_id, message)
