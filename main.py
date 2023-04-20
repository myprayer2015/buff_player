import codecs
import json
import csv
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.draw_chart import DrawChart
from src.buff_manager import BuffManager
from src.http_utils import HttpUtils
from src.message_tool import MessageTool
from src.config import settings
from src.storage.file_storage import FileStorage
import requests
from urllib.parse import quote

storage = FileStorage()
storage.connect()

with ThreadPoolExecutor(max_workers=1) as executor:
    with open('data/target_goods.txt', 'r', encoding='utf-8') as target_goods:
        full_name_list = []
        exterior_list = []
        quality_list = []
        for line in target_goods:
            item = line.split()
            full_name_list.append(item[0])
            exterior_list.append(item[1])
            quality_list.append(item[2])
        id_list = storage.get_ids_by_goods_info(full_name_list, exterior_list, quality_list)
        if len(id_list) == 0:
            print("empty id list")

        bmg = BuffManager()
        work_list = [executor.submit(bmg.get_sell_order, id) for id in id_list]
        for future in as_completed(work_list):
            data = future.result()
            print('get_sell_order: ', data)
        print('finished')

'''

message_tool = MessageTool()
file_str = file_reader.read()
message_tool.send_wechat(goods_name, file_str)

sleep_time = random.randint(settings.min_sleep_time, settings.max_sleep_time)
time.sleep(sleep_time)
drawer = DrawChart()
drawer.drawchart()
'''