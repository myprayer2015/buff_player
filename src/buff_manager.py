import urllib.request as re
from urllib.request import ProxyHandler, build_opener
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
from .utils.http_utils import HttpUtils
from .utils.time_utils import TimeUtils
from typing import Any


class BuffManager:
    game = settings.game
    user_agent = ""
    cookie = ""
    http_utils = HttpUtils()

    def __init__(self):
        self.http_utils.init()
        pass

    def select_all(self):
        with codecs.open('data/goods_info.csv', 'w', 'gbk', 'ignore') as csvfile:
            csv_writer = csv.writer(csvfile)

            page_num = 1
            while True:
                # try:
                # self.http_utils.init()
                # dynamic_proxy = self.http_utils.get_dynamic_proxy()
                # proxy_handler = ProxyHandler({
                #     'http': 'http://' + dynamic_proxy,
                #     'https': 'https://' + dynamic_proxy
                # })
                # print('dynamic_proxy=', dynamic_proxy)
                # opener = build_opener(proxy_handler)
                request = re.Request(
                    'https://buff.163.com/api/market/goods?game=%s&page_num=%s&page_size=500&sort_by=price.desc' % (self.game, str(page_num)))
                cookie = self.http_utils.get_cookie()
                request.add_header('cookie', cookie)
                request.add_header('User-Agent', UserAgent().random)
                get = re.urlopen(request)
                # get = opener.open(request)
                info = json.loads(get.read().decode('utf-8'))
                # except OSError as err:
                #     print("[select_all] OS error: {0}".format(err))
                #     info = None
                # except:
                #     print("[select_all] Unexpected error:", sys.exc_info()[0])
                #     info = None
                if not info or info['code'] != 'OK':
                    # print("code_is_not_ok, page_num=%d status=%s msg=%s reason=%s" % page_num, get.status, get.msg, get.reason)
                    if (info['code'] != 'OK'):
                        print("code_is_not_ok, page_num=%d" % page_num)
                        print('cookie=%s' % cookie)
                        print(info)
                    page_num += 1
                    time.sleep(10)
                    continue
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
                    # print(goods_id, goods_full_name, goods_internal_name, goods_exterior, goods_quality,
                    #                         goods_sell_num, goods_min_price)
                    csv_writer.writerow([goods_id, goods_full_name, goods_internal_name, 
                                            goods_exterior, goods_quality, goods_stattrak,
                                            goods_sell_num, goods_min_price])
                    csvfile.flush()

                if page_num == info['data']['total_page'] - 1:
                    break
                page_num += 1
                time.sleep(10)

    def get_info(self, goods_id):
        dynamic_proxy = self.http_utils.get_dynamic_proxy()
        if dynamic_proxy != "":
            handler = urllib.request.ProxyHandler(dynamic_proxy)
            opener = urllib.request.build_opener(handler)
            request = re.Request(
                'https://buff.163.com/api/market/goods/sell_order?game=%s&goods_id=%s' % (self.game, goods_id))
            request.add_header('cookie', self.http_utils.get_cookie())
            request.add_header('User-Agent',
                               UserAgent().random)
            get = opener.open(request)
            return get.read().decode('utf-8')

    def get_price(self, goods_id):
        dynamic_proxy = self.http_utils.get_dynamic_proxy()
        if dynamic_proxy != "":
            handler = urllib.request.ProxyHandler(dynamic_proxy)
            opener = urllib.request.build_opener(handler)
            request = re.Request(
                'https://buff.163.com/api/market/goods/sell_order?game=%s&goods_id=%s' % (self.game, goods_id))
            request.add_header('cookie', self.http_utils.get_cookie())
            request.add_header('User-Agent',
                               UserAgent().random)
            get = opener.open(request)
            info = json.loads(get.read().decode('utf-8'))
            json_str = json.dumps(info, indent=2)
            print(json_str)

    def get_num(self, goods_name):
        dynamic_proxy = self.http_utils.get_dynamic_proxy()
        if dynamic_proxy != "":
            try:
                handler = urllib.request.ProxyHandler(dynamic_proxy)
                opener = urllib.request.build_opener(handler)
                urlparse = urllib.parse.quote(goods_name)
                request = urllib.request.Request(
                    "https://buff.163.com/api/market/goods?game=%s&page_num=1&search=%s" % (self.game, urlparse))
                request.add_header('cookie', self.http_utils.get_cookie())
                request.add_header('User-Agent',
                                   UserAgent().random)
                get = opener.open(request)
                info = json.loads(get.read().decode('utf-8'))
            except OSError as err:
                print("[get_num] OS error: {0}".format(err))
                info = None
            except:
                print("[get_num] Unexpected error:", sys.exc_info()[0])
                info = None

            return info

    # 交易记录
    def get_bill_order(self, goods_id):
        dynamic_proxy = self.http_utils.get_dynamic_proxy()
        if dynamic_proxy != "":
            proxy_handler = ProxyHandler({
                'http': 'http://' + dynamic_proxy,
                'https': 'https://' + dynamic_proxy
            })
            # print(dynamic_proxy)
            opener = build_opener(proxy_handler)
            order_list = []
            page_num = 1
            page_size = 20
            while True:
                try:
                    request = re.Request(
                        'https://buff.163.com/api/market/goods/bill_order?game=%s&goods_id=%s&page_num=%s&page_size=%s' % (self.game, goods_id, str(page_num), str(page_size)))
                    request.add_header('cookie', self.http_utils.get_cookie())
                    request.add_header('User-Agent',
                                       UserAgent().random)
                    get = opener.open(request)
                    info = json.loads(get.read().decode('utf-8'))
                except OSError as err:
                    print("[get_bill_order] OS error: {0}".format(err))
                    info = None
                except:
                    print("[get_bill_order] Unexpected error:",
                          sys.exc_info()[0])
                if not info or info['code'] != 'OK':
                    return ''
                for item in info['data']['items']:
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
                    # print(id, price, type, buyer_id, seller_id, paintwear)
                total_page = info['data']['total_page']
                if page_num >= total_page:
                    break
                page_num += 1
            return order_list

    # 在售记录
    def get_sell_order(self, goods_id):
        time_utils = TimeUtils()
        
        order_list = []
        page_num = 1
        total_page = 3
        page_size = 20
        while True:
            time_utils.start()
            try:
                self.http_utils.reload()
                cookie = self.http_utils.get_cookie()
                dynamic_proxy = self.http_utils.get_dynamic_proxy()
                proxy_handler = ProxyHandler({
                    'http': 'http://' + dynamic_proxy,
                    'https': 'https://' + dynamic_proxy
                })
                opener = build_opener(proxy_handler)
                request = re.Request(
                    'https://buff.163.com/api/market/goods/sell_order?game=%s&goods_id=%s&page_num=%s&page_size=%s' % (self.game, goods_id, str(page_num), str(page_size)))
                request.add_header('cookie', cookie)
                # request.add_header('User-Agent', UserAgent().random)
                request.add_header(
                    'User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
                # get = re.urlopen(request)
                get = opener.open(request)
                info = json.loads(get.read().decode('utf-8'))
            except OSError as err:
                print("[os_error][get_sell_order] OS error: {0}, dynamic_proxy={1}".format(err, dynamic_proxy))
                info = None
            except:
                print("[unkown][get_sell_order] Unexpected error:", sys.exc_info()[0], " dynamic_proxy=", dynamic_proxy)
            if not info or info['code'] != 'OK':
                time_utils.stop()
                print("[code_is_not_ok][time_cost][get_sell_order] all_tm=%d avg_tm=%f dynamic_proxy=%s cookie=%s goods_id=%s" % (time_utils.get_all_time_ms(), time_utils.get_all_time_ms() * 1.0 / page_num, dynamic_proxy, cookie, goods_id))
                time_utils.stop()
                continue
            for item in info['data']['items']:
                order = []
                order.append(item['id'])
                order.append(item['price'])
                order.append(item['asset_info']['paintwear'])
                order.append(item['user_id'])
                order.append(item['created_at'])
                order.append(item['recent_average_duration'])
                order.append(item['recent_deliver_rate'])
                order.append(item['asset_info']['assetid'])
                order.append(item['asset_info']['classid'])
                order_list.append(order)
                # print(id, price, paintwear, user_id, created_at, recent_average_duration, recent_deliver_rate, asset_id, class_id)
            total_page = info['data']['total_page']
            if page_num >= total_page:
                time_utils.stop()
                break
            page_num += 1
        print("[time_cost][get_sell_order] all_tm=%d avg_tm=%f goods_id=%s" % (time_utils.get_all_time_ms(), time_utils.get_all_time_ms() * 1.0 / page_num, goods_id))
        return order_list

    # 求购记录
    def get_buy_order(self, goods_id):
        dynamic_proxy = self.http_utils.get_dynamic_proxy()
        if dynamic_proxy != "":
            proxy_handler = ProxyHandler({
                'http': 'http://' + dynamic_proxy,
                'https': 'https://' + dynamic_proxy
            })
            # print(dynamic_proxy)
            opener = build_opener(proxy_handler)
            order_list = []
            page_num = 1
            total_page = 3
            page_size = 20
            while True:
                try:
                    request = re.Request(
                        'https://buff.163.com/api/market/goods/buy_order?game=%s&goods_id=%s&page_num=%s&page_size=%s' % (self.game, goods_id, str(page_num), str(page_size)))
                    request.add_header('cookie', self.http_utils.get_cookie())
                    request.add_header('User-Agent',
                                       UserAgent().random)
                    get = opener.open(request)
                    info = json.loads(get.read().decode('utf-8'))
                except OSError as err:
                    print("[get_buy_order] OS error: {0}".format(err))
                    info = None
                except:
                    print("[get_buy_order] Unexpected error:",
                          sys.exc_info()[0])
                if not info or info['code'] != 'OK':
                    return ''
                for item in info['data']['items']:
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
                    # print(id, price, num, frozen_amount, created_at, user_id)
                total_page = info['data']['total_page']
                if page_num >= total_page:
                    break
                page_num += 1
            return order_list
