from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import codecs

from src.buff_manager import BuffManager
from src.storage.file_storage import FileStorage

from src.utils.http_util import HttpUtil
import threading
from time import sleep, time

from src.utils.time_util import TimeUtil

def dump_goods_info():
    bmg = BuffManager()
    bmg.select_all()
    return

def buff_manager_test():
    buf = BuffManager()
    print(buf.get_sell_order('776305'))

def get_goods_buff_data():
    storage = FileStorage()
    storage.connect()
    with ThreadPoolExecutor(max_workers=10) as executor:
        with open('data/target_goods.txt', 'r', encoding='gbk') as target_goods:
            full_name_list = []
            exterior_list = []
            quality_list = []
            internal_name_list = []
            stattrak_list = []
            flag = 0
            for line in target_goods:
                if flag == 0:
                    flag += 1
                    continue
                item = line.split()
                full_name_list.append(item[0])
                exterior_list.append(item[1])
                quality_list.append(item[2])
                internal_name_list.append(item[3])
                stattrak_list.append(item[4])
            id_list = storage.get_ids_by_goods_info(full_name_list, exterior_list, quality_list, internal_name_list, stattrak_list)
            print('len:', len(id_list))
            if len(id_list) == 0:
                print("empty id list")
            print("start to get sell_order of %d goods" % len(id_list))
            bmg = BuffManager()
            bmg.init()
            work_list = [executor.submit(bmg.get_sell_order, id) for id in id_list]
            for future in as_completed(work_list):
                data = future.result()
                print('[complete] id=%s' % data[0])
                sell_order_file = 'data/sell_order/' + data[0]
                with codecs.open(sell_order_file, 'w', 'gbk', 'ignore') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    for item in data[1]:
                        csv_writer.writerow(item)
            print('finished')

get_goods_buff_data()
# buff_manager_test()
# dump_goods_info()

'''

message_tool = MessageUtil()
file_str = file_reader.read()
message_tool.send_wechat(goods_name, file_str)

sleep_time = random.randint(settings.min_sleep_time, settings.max_sleep_time)
time.sleep(sleep_time)
drawer = DrawChart()
drawer.drawchart()
'''