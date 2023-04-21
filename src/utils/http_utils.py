import codecs
import random

from src.config import settings
import requests

class HttpUtils:
    cookies_list = []
    dynamic_proxy_list = []

    def __init__(self):
        pass

    def init(self):
        with open('data/cookies.txt', 'r') as f:
            for line in f.readlines():
                self.cookies_list.append(str(line).rstrip())

        with codecs.open('data/dynamic_ip_list.txt', 'w') as ip_writer:
            ret = requests.get(settings.dynamic_ip_api)
            # ip_writer.write(ret.text.replace('\n', ''))
            for ip_port in ret.text.split():
                self.dynamic_proxy_list.append(ip_port)

    def reload(self):
        with codecs.open('data/dynamic_ip_list.txt', 'w') as ip_writer:
            ret = requests.get(settings.dynamic_ip_api)
            # ip_writer.write(ret.text.replace('\n', ''))
            for ip_port in ret.text.split():
                self.dynamic_proxy_list.append(ip_port)
            print(ret.status_code, self.dynamic_proxy_list[0])


    def get_cookie(self):
        # return self.cookies_list[0]
        return self.cookies_list[random.randint(0, len(self.cookies_list) - 1)]

    def get_dynamic_proxy(self):
        return self.dynamic_proxy_list[random.randint(0, len(self.dynamic_proxy_list) - 1)]