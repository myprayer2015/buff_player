import codecs
import random
import requests
from urllib.request import ProxyHandler, build_opener
import urllib.request as re
from fake_useragent import UserAgent
import json
import sys
from readerwriterlock import rwlock

from src.config import settings
from .time_util import TimeUtil
from .message_util import MessageUtil

class HttpUtil:
    cookies_valid_map = {}
    cookies_list = []
    dynamic_proxy_list = []

    cookies_lock = rwlock.RWLockWriteD()
    cookies_read_lock = cookies_lock.gen_rlock()
    cookies_write_lock = cookies_lock.gen_wlock()

    proxy_lock = rwlock.RWLockWriteD()
    proxy_read_lock = proxy_lock.gen_rlock()
    proxy_write_lock = proxy_lock.gen_wlock()

    time_util = TimeUtil()
    
    message_util = MessageUtil()

    def __init__(self):
        pass

    def init(self):
        with open('data/cookies.txt', 'r') as f:
            for line in f.readlines():
                self.cookies_valid_map[str(line).rstrip()] = 1
                self.cookies_list.append(str(line).rstrip())
        # with codecs.open('data/dynamic_ip_list.txt', 'w') as ip_writer:
        #     ret = requests.get(settings.dynamic_ip_api)
        #     # ip_writer.write(ret.text.replace('\n', ''))
        #     for ip_port in ret.text.split():
        #         self.dynamic_proxy_list.append(ip_port)

        ret = requests.get(settings.dynamic_ip_api)
        for ip_port in ret.text.split():
            self.dynamic_proxy_list.append(ip_port)

    def reload(self):
        # with codecs.open('data/dynamic_ip_list.txt', 'w') as ip_writer:
        #     ret = requests.get(settings.dynamic_ip_api)
        #     # ip_writer.write(ret.text.replace('\n', ''))
        #     for ip_port in ret.text.split():
        #         self.dynamic_proxy_list.append(ip_port)
        #     print(ret.status_code, self.dynamic_proxy_list[0])
        while True:
            ret = requests.get(settings.dynamic_ip_api)
            if ret.status_code != 200:
                continue
            self.proxy_write_lock.acquire()
            self.dynamic_proxy_list.clear()
            for ip_port in ret.text.split():
                self.dynamic_proxy_list.append(ip_port)
            self.proxy_write_lock.release()
            break

    def update(self):
        with open('data/cookies.txt', 'w') as f:
            for cookie in self.cookies_list:
                f.write(cookie)
                f.write('\n')

    def get_cookie(self):
        self.cookies_read_lock.acquire()
        cookie = self.cookies_list[random.randint(0, len(self.cookies_list) - 1)]
        self.cookies_read_lock.release()
        return cookie

    def get_dynamic_proxy(self):
        self.proxy_read_lock.acquire()
        proxy = self.dynamic_proxy_list[random.randint(0, len(self.dynamic_proxy_list) - 1)]
        self.proxy_read_lock.release()
        return proxy

    def get(self, url):
        retry_num = 0
        cookie = ''
        dynamic_proxy = ''
        while True:
            if retry_num == settings.request_retry_warning_num:
                title = 'NetError'
                content = 'Retry too many times, cookie=' + cookie + ', proxy=' + dynamic_proxy + ', url=' + url
                self.message_util.send_wechat(title, content)
            if retry_num >= settings.request_retry_stop_num:
                break
            try:
                self.reload()
                cookie = self.get_cookie()
                dynamic_proxy = self.get_dynamic_proxy()
                proxy_handler = ProxyHandler({
                    'http': 'http://' + dynamic_proxy,
                    'https': 'https://' + dynamic_proxy
                })
                opener = build_opener(proxy_handler)
                request = re.Request(url)
                request.add_header('cookie', cookie)
                request.add_header('User-Agent', UserAgent().random)
                # get = re.urlopen(request)
                get = opener.open(request)
                info = json.loads(get.read().decode('utf-8'))
            except OSError as err:
                print("[os_error][get] OS error: {0}, dynamic_proxy={1}".format(err, dynamic_proxy))
                info = None
            except:
                print("[unkown][get] Unexpected error:", sys.exc_info()[0], " dynamic_proxy=", dynamic_proxy)
                info = None
            if not info or info['code'] != 'OK':
                if info:
                    # cookie±ª∑‚£¨≤ªÀ„÷ÿ ‘
                    if info['code'] == 'Action Forbidden':
                        self.cookies_write_lock.acquire()
                        self.cookies_list.remove(cookie)
                        self.cookies_valid_map.pop(cookie)
                        title = 'WrongCookie'
                        content = 'cookie is valid, cookie=' + cookie
                        self.message_util.send_wechat(title, content)
                        self.cookies_write_lock.release()
                        self.update()
                        print('invalid cookie:', cookie)
                        continue
                retry_num += 1
                continue
            else:
                return info
        return None