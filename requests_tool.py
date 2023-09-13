import requests
from urllib.parse import urlencode
class RequestsTool:
    def __init__(self,cookie, token, referer)-> None:
        self.header = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "Host": "learning.cbit.com.cn",
            "Referer": referer,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0",
            "X-Requested-With": "XMLHttpRequest",
            "apikey": "2456269a445b4a18afad29fd12714da2",
            "isapp": "0",
            "sec-ch-ua": '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "token": token,
        }
    def get(self,url)->str:
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            return  dict(response.json())
        else:
            print(str(response.status_code) + " get "+url)
            return '0'
    def post(self,data,url)->str:
        response = requests.post(url, data=data, headers=self.header)
        if response.status_code == 200:
            return  dict(response.json())
        else:
            print(str(response.status_code) + " post "+url)
            return '0'