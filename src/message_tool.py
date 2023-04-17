import requests
from src.config import settings

class MessageTool:
    def send_wechat(self, title, content):
        token = settings.pushplus_token
        template = 'markdown'
        url = f"https://www.pushplus.plus/send?token={token}&title={title}&content={content}&template={template}"
        r = requests.get(url=url)