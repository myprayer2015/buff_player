import requests
from fake_useragent import UserAgent

dynamic_ip_api = "http://api.proxy.ipidea.io/getBalanceProxyIp?num=10&return_type=txt&lb=1&sb=0&flow=1&regions=&protocol=http"
headers={'User-Agent':UserAgent().random}
ip_list = requests.post(dynamic_ip_api, headers=headers, verify=True)
proxie = "https://%s"%(ip_list.text.split()[0])
proxies = {'http': proxie}
print(proxies)

print(UserAgent().random)