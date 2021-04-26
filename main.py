import json
import requests
from datetime import datetime

import telebot


with open('secret.json', 'r') as f:
    secret = json.load(f)

token = secret['token']
chat_id = secret['chat_id']
ptx_url = "https://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/City/NewTaipei/"
headers = {
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
}

bot = telebot.TeleBot(token)


# query
api_data = requests.get(
    url=ptx_url + "%E8%97%8D23?$filter=StopName%2FZh_tw%20eq%20%27%E6%A8%9F%E6%A8%B9%E4%B8%80%E8%B7%AF%E5%8F%A3%27&$format=JSON",
    headers=headers
).json()

for data in api_data:
    if data['Direction'] != 0:  # 只處理往昆陽捷運站
        continue
    if data['EstimateTime'] / 60 > 10.0:  # 到站時間大於10分鐘不傳訊息
        continue

    update_time = datetime.strptime(data['UpdateTime'], '%Y-%m-%dT%H:%M:%S+08:00')
    # construct message
    message = "{}公車資訊\n".format(data['RouteName']['Zh_tw'])
    message += "{}\n".format(data['StopName']['Zh_tw'])
    message += "到站剩餘： {:.1f} 分鐘\n".format(data['EstimateTime'] / 60)
    message += "更新時間： {}\n".format(update_time.strftime('%H:%M'))

    bot.send_message(chat_id, message)
