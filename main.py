import urllib.parse
from urllib.parse import urlencode
from pprint import pprint
import AESCipher
from requests_tool import RequestsTool as RT
import random
import time
import json
import concurrent.futures
import requests


class Learn_Cbit:
    def __init__(self, name, cookie, token, tcid, passwrd='Abcd1234', speed=1.5) -> None:
        self.name = name
        self.passwrd = passwrd
        self.cookie = cookie
        self.token = token
        self.tcid = tcid
        self.speed = speed  # 1.5倍数
        print(self.name + ": 开启" + str(speed) + "倍速")

    def get_sessionIDCookie(self):
        base_url = r'https://learning.cbit.com.cn/www/views/checking.jsp'
        header = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
            "Connection": "keep-alive",
            "Host": "learning.cbit.com.cn",
            'Referer': " https: // learning.cbit.com.cn / www / views / index / index.html?sid = 0.8764445849584661",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }
        response = requests.get(base_url, headers=header)
        if response.status_code == 200:
            return dict(response.headers)['Set-Cookie'].split(', ')[-1].split('=')[-1]

    def login(self):
        pass

    def get_lessons_id(self) -> dict:
        base_url = "https://learning.cbit.com.cn/www/onlineTraining/trainingdetails.do?"
        data = {"id": self.tcid}
        url = base_url + urlencode(data)
        rt = RT(cookie=self.cookie, token=self.token, referer=url)
        result = rt.get(url=url)

        for i in range(10):
            if result is None or result.get('traininglesson') is None:
                result = rt.get(url=url)
            else:
                break
        return result["traininglesson"]

    def get_item_id(self, lessonID) -> dict:
        base_url = "https://learning.cbit.com.cn/www//lessonDetails/details.do"
        data = {"tcid": self.tcid, "lessonId": lessonID}
        #  url = base_url + urlencode(data)
        rt = RT(cookie=self.cookie, token=self.token,
                referer='https://learning.cbit.com.cn/www/views/lesson/lessonDetailsStudeyed.html?')
        result = rt.post(data, url=base_url)
        for i in range(10):
            if result.get('lessonitem') is None or result is None:
                result = rt.post(data, url=base_url)
            else:
                break
        return result["lessonitem"]

    def post_schedule(self, lessonId, itemId, tcid, totalTime, studyplan=0):
        base_url = (
            "https://learning.cbit.com.cn/www/lessonDetails/updateLessonProcessPC.do?"
        )
        studytime = totalTime * studyplan / 100
        while totalTime > studytime:
            print(f"{self.name}: 已经学习了{str(studytime)}秒，还剩{str(totalTime - studytime)}秒")
            random_num = random.randint(20, 80)
            time.sleep(random_num)
            studytime = (
                studytime + random_num * self.speed
                if totalTime > studytime + random_num * self.speed
                else totalTime
            )
            data = {
                "lessonId": lessonId,
                "lessonItemId": itemId,
                "process": "-2",
                "tcid": tcid,
                "totalTime": totalTime,
                "suspendTime": studytime,
                "studytime": studytime,
            }
            url = base_url + urlencode(data)
            rt = RT(cookie=self.cookie, token=self.token, referer=url)
            for i in range(3):
                result = rt.post(url=url, data=data)

    def learn(self):
        # 获得lessonID
        lessonsID = self.get_lessons_id()
        print(0)
        for lessonID in lessonsID:
            lession_infomation = self.get_item_id(lessonID["id"])
            for li in lession_infomation:
                if li["studyplan"] == 100:
                    print(f"{self.name}: 已经学过了：{li['itemname']}，自动跳过。")
                    continue
                print(f"{self.name}: 开始学习{li['itemname']}")
                self.post_schedule(
                    lessonID["id"],
                    li["id"],
                    self.tcid,
                    li["all_times"],
                    li["studyplan"],
                )


def learn_task(user_info):
    lc = Learn_Cbit(name=user_info['name'],
                    token=user_info['token'], cookie=user_info['cookie'], tcid=user_info['tcid'], speed=5)
    lc.learn()


if __name__ == "__main1__":
    file_path = 'D:\\Twikura\\token.json'
    with open(file_path, 'r') as file:
        users = json.load(file)
    max_threads = len(users)
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        for u in users:
            executor.submit(learn_task, u)

if __name__ == '__main__':
    base_url = 'https://learning.cbit.com.cn/www/views/checking.jsp?dt=' + urllib.parse.quote(' ' + time.strftime(
        "%a %b %d %Y %H:%M:%S")) + '%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'
    headers = {
        "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Encoding": 'gzip, deflate, br',
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
        "Host": "earning.cbit.com.cn",
        "Connection": "keep-alive",
        'Referer': r'https://learning.cbit.com.cn/www/views/index/index.html?sid=0.8764445849584661',
        'Sec-Fetch-Dest': "image",
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }
    print(base_url)
    url = r'https://learning.cbit.com.cn/www/views/checking.jsp?'
    # https://learning.cbit.com.cn/www/views/checking.jsp?dt= Fri Nov 03 2023 17:29:57 GMT+0800 (中国标准时间)
    data = {
        'dt': time.strftime("%a %b %d %Y %H:%M:%S") + ' GMT+0800 (中国标准时间)'
    }
    proxy = {
        'http': '127.0.0.1:8888',
    }
    response = requests.get(url=base_url, headers=headers, proxies=proxy,verify=False)
    if response.status_code == 200:
        print(dict(response.headers))
    else:
        print(response.status_code)
