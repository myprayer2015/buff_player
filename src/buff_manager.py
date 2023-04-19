import urllib.request as re
import urllib.parse
import json
import time
import csv
import codecs

from fake_useragent import UserAgent
from src.config import settings

class BuffManager:
    dynamic_ip_api = settings.dynamic_ip_api
    cookie = settings.cookie
    proxies = ""
    game = settings.game
    user_agent = ""

    def __init__(self):
        pass

    def init_dynamic_info(self):
        request = re.Request(self.dynamic_ip_api, method='POST')
        request.add_header('User-Agent',
                           self.user_agent)
        ip_list = re.urlopen(request)
        proxie = "https://%s" % (ip_list.read().decode('utf-8').split()[0])
        self.proxies = {'http': proxie}
        self.user_agent = UserAgent().random

    def select_all(self):
        if self.proxies != "":
            with codecs.open('data/goods_info.csv', 'w', 'gbk', 'ignore') as csvfile:
                csv_writer = csv.writer(csvfile)

                page_num = 1
                while True:
                    request = re.Request(
                        'https://buff.163.com/api/market/goods?game=%s&page_num=%s&page_size=500&sort_by=price.desc' % (self.game, str(page_num)))
                    request.add_header('cookie', self.cookie)
                    request.add_header('User-Agent',
                                       self.user_agent)
                    get = re.urlopen(request)
                    json_obj = json.loads(get.read().decode('utf-8'))

                    for item in json_obj['data']['items']:
                        goods_internal_name = "default_internal_name"
                        goods_exterior = "default_exterior"
                        goods_quality = "default_quality"

                        # 饰品在buff内部使用的name
                        if 'weapon' in item['goods_info']['info']['tags']:
                            goods_internal_name = item['goods_info']['info']['tags']['weapon']['internal_name']
                        # 饰品外观
                        if 'exterior' in item['goods_info']['info']['tags']:
                            goods_exterior = json.loads('"%s"' % item['goods_info']['info']['tags']['exterior']['localized_name'])
                        # 饰品是否是纪念品
                        if 'quality' in item['goods_info']['info']['tags']:
                            goods_quality = item['goods_info']['info']['tags']['quality']['localized_name']
                        # 饰品在buff内部的id
                        goods_id = item['id']
                        # 饰品的全名
                        goods_full_name = json.loads('"%s"' % item['name'])
                        goods_sell_num = item['sell_num']
                        goods_min_price = item['sell_min_price']
                        #goods_steam_market_url = item['steam_market_url']
                        print(goods_id, goods_full_name, goods_internal_name, goods_exterior, goods_quality,
                                                goods_sell_num, goods_min_price)
                        csv_writer.writerow([goods_id, goods_full_name, goods_internal_name, goods_exterior, goods_quality,
                                                goods_sell_num, goods_min_price])
                        csvfile.flush()


                    if page_num == json_obj['data']['total_page'] - 1:
                        break
                    page_num += 1
                    time.sleep(10)

    def get_info(self, goods_id):
        if self.proxies != "":
            request = re.Request(
                'https://buff.163.com/api/market/goods/sell_order?game=%s&goods_id=%s' % (self.game, goods_id))
            request.add_header('cookie', self.cookie)
            request.add_header('User-Agent',
                               self.user_agent)
            get = re.urlopen(request)
            return get.read().decode('utf-8')

    def get_price(self, goods_id):
        if self.proxies != "":
            request = re.Request(
                'https://buff.163.com/api/market/goods/sell_order?game=%s&goods_id=%s' % (self.game, goods_id))
            request.add_header('cookie', self.cookie)
            request.add_header('User-Agent',
                               self.user_agent)
            get = re.urlopen(request)
            info = json.loads(get.read().decode('utf-8'))
            json_str = json.dumps(info, indent=2)
            print(json_str)


    def get_num(self, goods_name):
        if self.proxies != "":
            urlparse = urllib.parse.quote(goods_name)
            request = urllib.request.Request(
                "https://buff.163.com/api/market/goods?game=%s&page_num=1&search=%s" % (self.game, urlparse))
            request.add_header('cookie', self.cookie)
            request.add_header('User-Agent',
                               self.user_agent)
            get = urllib.request.urlopen(request)
            return get.read().decode('utf-8')