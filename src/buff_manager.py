from hashlib import new
import os
from typing_extensions import Self
import urllib.request as re
import urllib.parse
import requests
import json
import time
import csv
import codecs
import random
from fake_useragent import UserAgent
from src.config import settings
import sys
from .utils.http_util import HttpUtil
from .utils.time_util import TimeUtil
from .utils.log_util import LogUtil
from typing import Any


class BuffManager:
    game = settings.game
    user_agent = ""
    cookie = ""
    http_util = HttpUtil()
    path_map = {}
    path_map['sell'] = settings.sell_order_data_dir
    path_map['bill'] = settings.bill_order_data_dir
    path_map['buy'] = settings.buy_order_data_dir

    def __init__(self):
        pass

    def init(self):
        self.http_util.init()

    def select_all(self):
        with codecs.open('data/goods_info.csv', 'w', 'gbk', 'ignore') as csvfile:
            csv_writer = csv.writer(csvfile)

            page_num = 1
            total_page = 253
            while True:
                url = 'https://buff.163.com/api/market/goods?game=%s&page_num=%s&page_size=500&sort_by=price.desc' % (self.game, str(page_num))
                info = self.http_util.get(url)

                if info:
                    for item in info['data']['items']:
                        goods_internal_name = "default_internal_name"
                        goods_exterior = "default_exterior"
                        goods_quality = "default_quality"
                        goods_stattrak = "normal"
                        # 饰品在buff内部使用的name
                        if 'weapon' in item['goods_info']['info']['tags']:
                            goods_internal_name = item['goods_info']['info']['tags']['weapon']['internal_name']
                        # 饰品外观
                        if 'exterior' in item['goods_info']['info']['tags']:
                            goods_exterior = json.loads(
                                '"%s"' % item['goods_info']['info']['tags']['exterior']['internal_name'])
                        # 饰品是否是纪念品
                        if 'quality' in item['goods_info']['info']['tags']:
                            goods_quality = item['goods_info']['info']['tags']['quality']['internal_name']
                        # 饰品在buff内部的id
                        goods_id = item['id']
                        # 饰品的全名
                        goods_full_name = json.loads('"%s"' % item['name'])
                        if 'StatTrak' in goods_full_name:
                            goods_stattrak = 'stattrak'
                        goods_sell_num = item['sell_num']
                        goods_min_price = item['sell_min_price']
                        # goods_steam_market_url = item['steam_market_url']
                        # LogUtil.info(goods_id, goods_full_name, goods_internal_name, goods_exterior, goods_quality,
                        #                         goods_sell_num, goods_min_price)
                        csv_writer.writerow([goods_id, goods_full_name, goods_internal_name,
                                                goods_exterior, goods_quality, goods_stattrak,
                                                goods_sell_num, goods_min_price])
                        csvfile.flush()
                else:
                    LogUtil.warning('[select_all] fail to get %d page' % page_num)
                    page_num += 1
                    continue
                total_page = info['data']['total_page']
                if page_num >= total_page:
                    break
                page_num += 1
                time.sleep(5)
        
    def get_newest_recorder(self, order_type, goods_id):
        goods_file = self.path_map[order_type] + goods_id
        if os.path.isfile(goods_file):
            with codecs.open(goods_file, 'r', 'gbk', 'ignore') as csvfile:
                csv_reader = csv.reader(csvfile)
                for line in csv_reader:
                    return line
        else:
            return None

    def get_bill_order(self, goods_id):
        time_util = TimeUtil()
        order_list = []
        page_num = 1
        total_page = 1
        page_size = 20
        newest_recorder = self.get_newest_recorder('sell', goods_id)
        if newest_recorder:
            newest_tmp = int(newest_recorder[4])
        else:
            newest_tmp = -1
        continue_get_flag = True
        while True:
            time_util.start()
            url = 'https://buff.163.com/api/market/goods/bill_order?game=%s&goods_id=%s&page_num=%s&page_size=%s' % (self.game, goods_id, str(page_num), str(page_size))
            info = self.http_util.get(url)
            if info:
                for item in info['data']['items']:
                    cur_tmp = int(item['created_at'])
                    if cur_tmp < newest_tmp:
                        continue_get_flag = False
                        break
                    elif cur_tmp == newest_tmp:
                        if newest_recorder[0] == item['id'] \
                            or newest_recorder[3] == item['user_id'] \
                            or newest_recorder[7] == item['asset_info']['assetid'] \
                            or newest_recorder[8] == item['asset_info']['classid']:
                            continue_get_flag = False
                            break
                    order = []
                    order.append(item['asset_info']['id'])
                    order.append(item['price'])
                    # 磨损度
                    order.append(item['asset_info']['paintwear'])
                    order.append(item['buyer_pay_time'])
                    order.append(item['created_at'])
                    # 交易完成时间
                    order.append(item['transact_time'])
                    # 交易完成后，饰品的解冻时间)
                    order.append(item['tradable_unfrozen_time'])
                    order.append(item['instanceid'])
                    order.append(item['asset_info']['assetid'])
                    order.append(item['asset_info']['classid'])
                    # 1为出售，2为供应
                    order.append(item['type'])
                    order.append(item['buyer_id'])
                    order.append(item['seller_id'])
                    order_list.append(order)
                    # LogUtil.info(id, price, paintwear, user_id, created_at, recent_average_duration, recent_deliver_rate, asset_id, class_id)
                total_page = info['data']['total_page']
            else:
                LogUtil.warning('[get_bill_order] fail to get info, id=%s' % goods_id)
            if page_num >= total_page:
                time_util.stop()
                break
            time_util.stop()
            if continue_get_flag == False:
                break
            page_num += 1
        LogUtil.info("[get_bill_order] all_tm=%d avg_tm=%f goods_id=%s" % (time_util.get_all_time_ms(), time_util.get_avg_time_ms(), goods_id))
        return order_list

    # 在售记录
    def get_sell_order(self, goods_id):
        time_util = TimeUtil()
        order_list = []
        page_num = 1
        total_page = 1
        page_size = 20
        newest_recorder = self.get_newest_recorder('sell', goods_id)
        # if newest_recorder:
        #     newest_created_tmp = int(newest_recorder[4])
        #     newest_updated_tmp = int(newest_recorder[5])
        # else:
        #     newest_created_tmp = -1
        #     newest_updated_tmp = -1
        continue_get_flag = True
        while True:
            time_util.start()
            url = 'https://buff.163.com/api/market/goods/sell_order?game=%s&goods_id=%s&page_num=%s&page_size=%s&sort_by=created.desc' % (self.game, goods_id, str(page_num), str(page_size))
            print(url)
            info = self.http_util.get(url, goods_id, page_num)
            print(info)
            if info:
                for item in info['data']['items']:
                    cur_created_tmp = int(item['created_at'])
                    order = []
                    order.append(item['id'])
                    order.append(item['price'])
                    order.append(item['asset_info']['paintwear'])
                    order.append(item['user_id'])
                    order.append(item['created_at'])
                    order.append(item['updated_at'])
                    order.append(item['recent_average_duration'])
                    order.append(item['recent_deliver_rate'])
                    order.append(item['asset_info']['assetid'])
                    order.append(item['asset_info']['classid'])
                    order_list.append(order)
                    # if cur_created_tmp < newest_created_tmp:
                    #     continue_get_flag = False
                    #     LogUtil.info('1, cur_tmp=%d, newest_tmp=%d'% (cur_created_tmp, newest_created_tmp))
                    #     LogUtil.info(order)
                    #     break
                    # elif cur_created_tmp == newest_created_tmp:
                    #     if newest_recorder[0] == item['id'] \
                    #         or newest_recorder[3] == item['user_id'] \
                    #         or newest_recorder[7] == item['asset_info']['assetid'] \
                    #         or newest_recorder[8] == item['asset_info']['classid']:
                    #         continue_get_flag = False
                    #         LogUtil.info('2')
                    #         LogUtil.info(order)
                    #         break
                    # LogUtil.info(id, price, paintwear, user_id, created_at, recent_average_duration, recent_deliver_rate, asset_id, class_id)
                total_page = info['data']['total_page']
            else:
                LogUtil.warning('[get_sell_order] fail to get info, id=%s page_num=%d' % (goods_id, page_num))
            if page_num >= total_page:
                time_util.stop()
                break
            time_util.stop()
            if continue_get_flag == False:
                LogUtil.info("flag_is_false")
                break
            page_num += 1
            if page_num > 1:
                break
        LogUtil.info("[get_sell_order] all_tm=%d avg_tm=%f goods_id=%s" % (time_util.get_all_time_ms(), time_util.get_avg_time_ms(), goods_id))
        return goods_id, order_list

    # 求购记录
    def get_buy_order(self, goods_id):
        time_util = TimeUtil()
        order_list = []
        page_num = 1
        total_page = 1
        page_size = 20
        newest_recorder = self.get_newest_recorder('sell', goods_id)
        if newest_recorder:
            newest_tmp = int(newest_recorder[4])
        else:
            newest_tmp = -1
        continue_get_flag = True
        while True:
            time_util.start()
            url = 'https://buff.163.com/api/market/goods/buy_order?game=%s&goods_id=%s&page_num=%s&page_size=%s' % (self.game, goods_id, str(page_num), str(page_size))
            info = self.http_util.get(url)
            if info:
                for item in info['data']['items']:
                    cur_tmp = int(item['created_at'])
                    if cur_tmp < newest_tmp:
                        continue_get_flag = False
                        break
                    elif cur_tmp == newest_tmp:
                        if newest_recorder[0] == item['id'] \
                            or newest_recorder[3] == item['user_id'] \
                            or newest_recorder[7] == item['asset_info']['assetid'] \
                            or newest_recorder[8] == item['asset_info']['classid']:
                            continue_get_flag = False
                            break
                    order = []
                    order.append(item['id'])
                    order.append(item['price'])
                    # 求购数量
                    order.append(item['num'])
                    # 求购价格
                    order.append(item['frozen_amount'])
                    order.append(item['created_at'])
                    order.append(item['user_id'])
                    if 'specific' in item and 'values' in item['specific'] and item['specific']['type'] == 'paintwear':
                        order.append(item['specific']['value'][0])
                        order.append(item['specific']['value'][1])
                    order_list.append(order)
                    # LogUtil.info(id, price, paintwear, user_id, created_at, recent_average_duration, recent_deliver_rate, asset_id, class_id)
                total_page = info['data']['total_page']
            else:
                LogUtil.warning('[get_buy_order] fail to get info, id=%s' % goods_id)
            if page_num >= total_page:
                time_util.stop()
                break
            time_util.stop()
            if continue_get_flag == False:
                break
            page_num += 1
        LogUtil.info("[get_buy_order] all_tm=%d avg_tm=%f goods_id=%s" % (time_util.get_all_time_ms(), time_util.get_avg_time_ms(), goods_id))
        return order_list