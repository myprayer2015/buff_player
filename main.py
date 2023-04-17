import json
import csv
import time
import random
from src.draw_chart import DrawChart
from src.buff_manager import BuffManager
from src.message_tool import MessageTool
from src.config import settings

goods_id = "42495"

file = open("data/HistoryPrice.txt", 'a')
file_reader = open("data/HistoryPrice.txt", 'r')
csvfile = open('data/HistoryPrice.csv', 'a', newline='')
csv_writer = csv.writer(csvfile)

while True:
    bmg = BuffManager()
    bmg.init_dynamic_info()
    InfoJson = bmg.get_info(goods_id)
    info = json.loads(InfoJson)

    info_data = info['data']
    info_items = info_data['items']
    info_item = info_items[0]
    info_price = info_item['price']
    goods_infos = info_data['goods_infos']
    goods_info = goods_infos[goods_id]
    goods_name = goods_info['name']

    NumJson = bmg.get_num(goods_name)
    num = json.loads(NumJson)

    num_data = num['data']
    num_items = num_data['items']
    num_item = num_items[0]
    sell_num = num_item['sell_num']

    ticks = time.strftime('%Y年%m月%d日%H:%M:%S', time.localtime())

    file.write("%s %s %s\n" % (ticks, info_price, sell_num))
    csv_writer.writerow([ticks, info_price, sell_num])
    #print("%s %s %s" % (ticks, info_price, sell_num))
    file.flush()
    csvfile.flush()

    message_tool = MessageTool()
    file_str = file_reader.read()
    message_tool.send_wechat(goods_name, file_str)

    sleep_time = random.randint(settings.min_sleep_time, settings.max_sleep_time)
    time.sleep(sleep_time)
    drawer = DrawChart()
    drawer.drawchart()