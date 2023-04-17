import urllib.request as re
import urllib.parse
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

    def get_info(self, goods_id):
        if self.proxies != "":
            request = re.Request(
                'https://buff.163.com/api/market/goods/sell_order?game=%s&goods_id=%s' % (self.game, goods_id))
            request.add_header('cookie', self.cookie)
            request.add_header('User-Agent',
                               self.user_agent)
            get = re.urlopen(request)
            return get.read().decode('utf-8')

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