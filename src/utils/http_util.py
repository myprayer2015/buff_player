import codecs
import random
from time import sleep, time
import requests
from urllib.request import ProxyHandler, build_opener
import urllib.request as re
from fake_useragent import UserAgent
import json
import sys
from readerwriterlock import rwlock
import threading
import atexit

from src.config import settings
from .time_util import TimeUtil
from .message_util import MessageUtil

class HttpUtil:
    cookies_list = []
    cookies_lock_map = {}
    cookies_condition = threading.Condition()
    
    dynamic_proxy_list = []
    dynamic_proxy_lock_map = {}

    time_util = TimeUtil()
    
    message_util = MessageUtil()

    def __init__(self):
        pass

    def init(self):
        with open('data/cookies.txt', 'r') as f:
            for line in f.readlines():
                self.cookies_lock_map[str(line).rstrip()] = [threading.Condition(), 1, self.time_util.get_current_time_ms()]
                self.cookies_list.append(str(line).rstrip())
        # with codecs.open('data/dynamic_ip_list.txt', 'w') as ip_writer:
        #     ret = requests.get(settings.dynamic_ip_api)
        #     # ip_writer.write(ret.text.replace('\n', ''))
        #     for ip_port in ret.text.split():
        #         self.dynamic_proxy_list.append(ip_port)

        # ret = requests.get(settings.dynamic_ip_api)
        # for ip_port in ret.text.split():
        #     self.dynamic_proxy_list.append(ip_port)
        pass

    def reload(self):
        # with codecs.open('data/dynamic_ip_list.txt', 'w') as ip_writer:
        #     ret = requests.get(settings.dynamic_ip_api)
        #     # ip_writer.write(ret.text.replace('\n', ''))
        #     for ip_port in ret.text.split():
        #         self.dynamic_proxy_list.append(ip_port)
        #     print(ret.status_code, self.dynamic_proxy_list[0])
        # while True:
        #     ret = requests.get(settings.dynamic_ip_api)
        #     if ret.status_code != 200:
        #         continue
        #     self.dynamic_proxy_list.clear()
        #     for ip_port in ret.text.split():
        #         self.dynamic_proxy_list.append(ip_port)
        #     break
        pass

    def update(self):
        print('update before quit, len=%d' % len(self.cookies_list))
        with open('data/cookies.txt', 'w') as f:
            for cookie in self.cookies_list:
                if self.cookies_lock_map[cookie][1] == 1:
                    f.write(cookie)
                    f.write('\n')

    def get_cookie(self):
        cookie = ''
        while cookie == '':
            for item in self.cookies_list:
                if (self.cookies_lock_map[item][1] == 1 and \
                        self.cookies_lock_map[item][0].acquire(False)):
                    if self.cookies_lock_map[item][1] == 1:
                        cookie = item
                        cnt = 1
                        while cnt < 10000:
                            cnt += 1
                        break
            if cookie == '':
                sleep(0.5)
                # self.cookies_lock_map[self.cookies_list[random.randint(0, len(self.cookies_list) - 1)]][0].wait()
                # self.cookies_lock_map[cookie][0].wait()
        return cookie

    def get_dynamic_proxy(self):
        proxy = ''
        while True:
            ret = requests.get(settings.dynamic_ip_api)
            if ret.status_code != 200:
                continue
            else:
                text_len = len(ret.text.split())
                proxy = ret.text.split()[random.randint(0, text_len - 1)]
                break
        return proxy

    def get(self, url, goods_id, page_num):
        retry_num = 0
        cookie = ''
        dynamic_proxy = ''
        proxy_time_util = TimeUtil()
        open_time_util = TimeUtil()
        while True:
            if retry_num == settings.request_retry_warning_num:
                title = 'NetError'
                content = 'Retry too many times, cookie=' + cookie + ', proxy=' + dynamic_proxy + ', url=' + url
                print('[get] Retry too many times, just warning, goods_id=%s, page_num=%d retry_num=%d' % (goods_id, page_num, retry_num))
                self.message_util.send_wechat(title, content)
            if retry_num >= settings.request_retry_stop_num:
                print('[get] Retry too many times, need break, goods_id=%s, page_num=%d retry_num=%d' % (goods_id, page_num, retry_num))
                break
            try:
                cookie = self.get_cookie()
                proxy_time_util.start()
                dynamic_proxy = self.get_dynamic_proxy()
                proxy_time_util.stop()
                proxy_handler = ProxyHandler({
                    'http': 'http://' + dynamic_proxy,
                    'https': 'https://' + dynamic_proxy
                })
                opener = build_opener(proxy_handler)
                request = re.Request(url)
                request.add_header('cookie', cookie)
                request.add_header('User-Agent', UserAgent().random)
                # get = re.urlopen(request)
                open_time_util.start()
                get = opener.open(request)
                open_time_util.stop()
                info = json.loads(get.read().decode('utf-8'))
            except OSError as err:
                print("[os_error][get] OS error: {0}, dynamic_proxy={1}, url={2}, goods_id={3}, page_num={4}".format(err, dynamic_proxy, url, goods_id, page_num))
                info = None
            except:
                print("[unkown][get] Unexpected error:", sys.exc_info()[0], " dynamic_proxy=", dynamic_proxy, " url=", url, " goods_id=", goods_id, " page_num=", page_num)
                info = None
            if not info or info['code'] != 'OK':
                if info:
                    # cookie±ª∑‚£¨≤ªÀ„÷ÿ ‘
                    if info['code'] == 'Action Forbidden':
                        self.cookies_lock_map[cookie][1] = 0
                        title = 'WrongCookie'
                        content = 'cookie is valid, cookie=' + cookie
                        self.message_util.send_wechat(title, content)
                        print('invalid cookie:', cookie)
                        self.cookies_lock_map[cookie][0].release()
                        continue
                    else:
                        print('[http_util][get] info is invalid, info=%s cookie=%s' % (info, cookie))
                    
                retry_num += 1
                continue
            else:
                print("[http_util][get] get_proxy_avg_tm=%f open_avg_tm=%f" % (proxy_time_util.get_avg_time_ms(), open_time_util.get_avg_time_ms()))
                self.cookies_lock_map[cookie][0].release()
                return info
        print("[http_util][get] get_proxy_avg_tm=%f open_avg_tm=%f" % (proxy_time_util.get_avg_time_ms(), open_time_util.get_avg_time_ms()))
        self.cookies_lock_map[cookie][0].release()
        return None