import json
import csv
import time
import random
import concurrent.futures

from src.draw_chart import DrawChart
from src.buff_manager import BuffManager
from src.message_tool import MessageTool
from src.config import settings
from src.storage.file_storage import FileStorage

goods_id = "42495"

file = open("data/HistoryPrice.txt", 'a')
file_reader = open("data/HistoryPrice.txt", 'r')
csvfile = open('data/HistoryPrice.csv', 'a', newline='')
csv_writer = csv.writer(csvfile)

while True:
    bmg = BuffManager()
    bmg.init_dynamic_info()
    break

    # file_storage = FileStorage()
    # file_storage.connect()
    # break

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        storage = FileStorage()
        storage.connect()
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
            bmg.init_dynamic_info()
            for id in id_list:
                print("get_buy_info, id=%s" % id)
                bmg.get_sell_order(id)

        # future_to_url = {executor.submit(load_url, url): url for url in URLS}
        # for future in concurrent.futures.as_completed(future_to_url):
        #     url = future_to_url[future]
        #     try:
        #         # 循环的获取认任务执行的结果
        #         data = future.result()
        #     except Exception as exc:
        #         print('generated an exception')
        #     else:
        #         print('页面内容省略')

    # bmg = BuffManager()
    # bmg.init_dynamic_info()
    # bmg.get_sell_order(44999)
    # bmg.get_buy_order(44999)
    break

    '''
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
    '''