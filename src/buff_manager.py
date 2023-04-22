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
from .utils.http_util import HttpUtil
from .utils.time_util import TimeUtil
from typing import Any


class BuffManager:
    game = settings.game
    user_agent = ""
    cookie = ""
    http_util = HttpUtil()
    http_util.init()

    def __init__(self):
        pass

    def select_all(self):
        with codecs.open('data/goods_info.csv', 'w', 'gbk', 'ignore') as csvfile:
            csv_writer = csv.writer(csvfile)

            page_num = 1
            total_page = 253
            while True:
                url = 'https://buff.163.com/api/market/goods?game=%s&page_num=%s&page_size=500&sort_by=price.desc' % (self.game, str(page_num))

                info = self.http_util.get(url)

                # try:
                # self.http_util.init()
                # dynamic_proxy = self.http_util.get_dynamic_proxy()
                # proxy_handler = ProxyHandler({
                #     'http': 'http://' + dynamic_proxy,
                #     'https': 'https://' + dynamic_proxy
                # })
                # print('dynamic_proxy=', dynamic_proxy)
                # opener = build_opener(proxy_handler)
                # request = re.Request(
                #     'https://buff.163.com/api/market/goods?game=%s&page_num=%s&page_size=500&sort_by=price.desc' % (self.game, str(page_num)))
                # cookie = self.http_util.get_cookie()
                # cookie = 'session=1-s2oIkHw4ds09AhH0tYBaS8DdljDPt8L23toxooxWKcej2032452555;P_INFO=17102442897|1675011638|1|netease_buff|00&99|null&null&null#zhj&330400#10#0|&0||17102442897;csrf_token=ImUyM2QxYjFjM2U3ZDRhNzhjMzllOGU1OTZjMWYzOTc2MDM0MzZiYTIi.Frg3ug.7LOxex-xSq9p71oaaiCz5mwGMTM;S_INFO=1675011638|0|0&60##|17102442897;NTES_YD_SESS=TEXGS.R3X00.lmb5zpmVFzb5Y.NcO25.cMQaCXx.RR83Eox_E6mDytyx_R.ChsXgNzmoPhJWchi2uTQCgWI49eixLuVoUweAyVlW7f..osXOXyKcoGenE1vnTrUIYObdPTm_nvhFRynbnoSr6EZkFO06StfH5Rw8s8VG1Gr4KQv5K0qO6nV7wwXP2VRbP6tHEYZPFUfEWPXAONqZ_67NJBBdzMzJBuXKIqe7wNtk1onp1;game=csgo;remember_me=U1105878163|GhlKObnWvDMQvnsDTcM4y3aCFKGGOTqF;Locale-Supported=zh-Hans;Device-Id=nxH7HYSLNQwx4s6DdLPV1'
                # cookie = 'session=1-CQknrsMzWmdOHZNxuz2TTeHq8tqxoCweunVrw76AsFF52032861442;P_INFO=17097097718|1676387260|1|netease_buff|00&99|null&null&null#zhj&330400#10#0|&0||17097097718;csrf_token=ImNkYjMwNWMwMjhkNTMyNjY3NTUwZGIzMmMwOTcyMmRiYTEwYmJiODIi.Fs01QQ.c3fKFtsYXydhrKtqcF6XLqFc6IQ;S_INFO=1676387260|0|0&60##|17097097718;NTES_YD_SESS=54QTivQi74MIrvWGec4zXvVAe9lINqF0omzM2HOV2SAqLRgoLmWedXs7NevTz9o_KxzJZgLfyymhMwuBzeW8ezk42dq5H1S1frBfTE7b0IGf_U6UicGlX3KE.mIus3yLEIuHI6xdvqc5z0exKh_PBcPlxM5hTDEpvb7MzkoY6T00ao32J5asd2JL6FQtDGK2x6LndTuTuAzUTCXkI5.EoSDtSzlLthZaqZTT8YG2mkS0a;game=csgo;remember_me=U1105567322|m8twgBbrLkrd5HudpLvHs6cckYxoXSDU;Locale-Supported=zh-Hans;Device-Id=KfKj9kXGIL8PjjjyPM0s'
                # cookie = 'session=1-N579FHGwktWN3TKyrKygNC-QUPWn6RnYfG2jf0MXQePS2032861489;P_INFO=16521767343|1676387447|1|netease_buff|00&99|null&null&null#zhj&330400#10#0|&0||16521767343;csrf_token=IjA1N2QxMTk2YWQxYzM4NDBjM2M1YjYzYmMwZTlmN2QzOGNkMjM5M2Ii.Fs01_A.iSUwJjZcTLaRM4EbL-iU-kvvyxQ;S_INFO=1676387447|0|0&60##|16521767343;NTES_YD_SESS=.WwYB7eKQpx43jHPza6_8ASu.066LPS4wPfTRyB_RD7gmVb8mPEkn1bVm6WfL0bssvOFk49P_PaasJ9pntSugEPMpgmXiyLwMHJOu8QN_Zg0DtuH.fCoRTS64PK5exrm6K5yK9YnhgQ.fAkYuoHspQsvYT.owj6WhOMTfC8U9wARGDZYxQ3FU7aR8FTjjGkEgyv9q42G2DnHBPGTk3E46CxTy4xx6CZ2APGrpWpe8z0pt;game=csgo;remember_me=U1105567337|KcEUo8mg4rdfWs3yOnyFkBGz4yAcGoxk;Locale-Supported=zh-Hans;Device-Id=B0KSGMkQ3JzohBe98trR'
                # request.add_header('cookie', cookie)
                # request.add_header('User-Agent', UserAgent().random)
                # get = re.urlopen(request)
                # get = opener.open(request)
                # info = json.loads(get.read().decode('utf-8'))
                # except OSError as err:
                #     print("[select_all] OS error: {0}".format(err))
                #     info = None
                # except:
                #     print("[select_all] Unexpected error:", sys.exc_info()[0])
                #     info = None
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
                        # print(goods_id, goods_full_name, goods_internal_name, goods_exterior, goods_quality,
                        #                         goods_sell_num, goods_min_price)
                        csv_writer.writerow([goods_id, goods_full_name, goods_internal_name,
                                                goods_exterior, goods_quality, goods_stattrak,
                                                goods_sell_num, goods_min_price])
                        csvfile.flush()
                else:
                    print('[select_all] fail to get %d page' % page_num)
                    page_num += 1
                    continue
                total_page = info['data']['total_page']
                if page_num >= total_page:
                    break
                page_num += 1
                time.sleep(5)

    def get_info(self, goods_id):
        dynamic_proxy = self.http_util.get_dynamic_proxy()
        if dynamic_proxy != "":
            handler = urllib.request.ProxyHandler(dynamic_proxy)
            opener = urllib.request.build_opener(handler)
            request = re.Request(
                'https://buff.163.com/api/market/goods/sell_order?game=%s&goods_id=%s' % (self.game, goods_id))
            request.add_header('cookie', self.http_util.get_cookie())
            request.add_header('User-Agent',
                               UserAgent().random)
            get = opener.open(request)
            return get.read().decode('utf-8')

    def get_price(self, goods_id):
        dynamic_proxy = self.http_util.get_dynamic_proxy()
        if dynamic_proxy != "":
            handler = urllib.request.ProxyHandler(dynamic_proxy)
            opener = urllib.request.build_opener(handler)
            request = re.Request(
                'https://buff.163.com/api/market/goods/sell_order?game=%s&goods_id=%s' % (self.game, goods_id))
            request.add_header('cookie', self.http_util.get_cookie())
            request.add_header('User-Agent',
                               UserAgent().random)
            get = opener.open(request)
            info = json.loads(get.read().decode('utf-8'))
            json_str = json.dumps(info, indent=2)
            print(json_str)

    def get_num(self, goods_name):
        dynamic_proxy = self.http_util.get_dynamic_proxy()
        if dynamic_proxy != "":
            try:
                handler = urllib.request.ProxyHandler(dynamic_proxy)
                opener = urllib.request.build_opener(handler)
                urlparse = urllib.parse.quote(goods_name)
                request = urllib.request.Request(
                    "https://buff.163.com/api/market/goods?game=%s&page_num=1&search=%s" % (self.game, urlparse))
                request.add_header('cookie', self.http_util.get_cookie())
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

    def get_bill_order(self, goods_id):
        time_util = TimeUtil()
        order_list = []
        page_num = 1
        total_page = 1
        page_size = 20
        while True:
            time_util.start()
            url = 'https://buff.163.com/api/market/goods/bill_order?game=%s&goods_id=%s&page_num=%s&page_size=%s' % (self.game, goods_id, str(page_num), str(page_size))
            info = self.http_util.get(url)
            if info:
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
                    order_list.append(order)
                    # print(id, price, paintwear, user_id, created_at, recent_average_duration, recent_deliver_rate, asset_id, class_id)
                total_page = info['data']['total_page']
            else:
                print('[get_sell_order] fail to get info, id=%s' % goods_id)
            if page_num >= total_page:
                time_util.stop()
                break
            time_util.stop()
            page_num += 1
        print("[get_bill_order] all_tm=%d avg_tm=%f goods_id=%s" % (time_util.get_all_time_ms(), time_util.get_avg_time_ms(), goods_id))
        return order_list

    # 在售记录
    def get_sell_order(self, goods_id):
        time_util = TimeUtil()
        order_list = []
        page_num = 1
        total_page = 1
        page_size = 20
        while True:
            time_util.start()
            url = 'https://buff.163.com/api/market/goods/sell_order?game=%s&goods_id=%s&page_num=%s&page_size=%s' % (self.game, goods_id, str(page_num), str(page_size))
            info = self.http_util.get(url)
            if info:
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
            else:
                print('[get_sell_order] fail to get info, id=%s' % goods_id)
            if page_num >= total_page:
                time_util.stop()
                break
            time_util.stop()
            page_num += 1
        print("[get_sell_order] all_tm=%d avg_tm=%f goods_id=%s" % (time_util.get_all_time_ms(), time_util.get_avg_time_ms(), goods_id))
        return order_list

    # 求购记录
    def get_buy_order(self, goods_id):
        time_util = TimeUtil()
        order_list = []
        page_num = 1
        total_page = 1
        page_size = 20
        while True:
            time_util.start()
            url = 'https://buff.163.com/api/market/goods/buy_order?game=%s&goods_id=%s&page_num=%s&page_size=%s' % (self.game, goods_id, str(page_num), str(page_size))
            info = self.http_util.get(url)
            if info:
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
                    # print(id, price, paintwear, user_id, created_at, recent_average_duration, recent_deliver_rate, asset_id, class_id)
                total_page = info['data']['total_page']
            else:
                print('[get_buy_order] fail to get info, id=%s' % goods_id)
            if page_num >= total_page:
                time_util.stop()
                break
            time_util.stop()
            page_num += 1
        print("[get_buy_order] all_tm=%d avg_tm=%f goods_id=%s" % (time_util.get_all_time_ms(), time_util.get_avg_time_ms(), goods_id))
        return order_list