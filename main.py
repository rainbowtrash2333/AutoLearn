import urllib.parse
from urllib.parse import urlencode
from pprint import pprint
from AESCipher import AESCipher
import requests_tool as RT
import random
import time
import json
import concurrent.futures
import requests
import shutil
from PIL import Image
import io
import easyocr
import logging


class Learn_Cbit:
    # name 登录名，一般为电话号码
    # tcid 课程id
    # passwd 登录密码, 默认为Abcd1234
    # speed 刷课速度，默认为1.5倍数
    # level filename filemode  日志系统参数
    def __init__(self, name, tcid, passwrd='Abcd1234', speed=1.5, level=logging.INFO, filename='app.log',
                 filemode='a') -> None:
        self.name = name
        self.passwrd = passwrd
        self.tcid = tcid
        self.speed = speed  # 1.5倍数
        self.headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        }
        logging.basicConfig(level=level,  # 设置日志级别，可以是DEBUG、INFO、WARNING、ERROR、CRITICAL
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            filename=filename,  # 将日志记录到文件中
                            filemode=filemode,
                            encoding='utf-8')
        console_handler = logging.StreamHandler()  # 创建控制台处理程序
        self.logger = logging.getLogger('my_app')
        self.logger.addHandler(console_handler)
        self.logger.info(f'{self.name}: 开启{str(speed)}倍速')

    def login(self):
        OCRreader = easyocr.Reader(['ch_sim'])
        encryption = AESCipher('dacf107e4bdbbef0', 'bcancid682e09aec')
        self.logger.debug(f"{self.name}尝试登录")
        verification_code_url = 'https://learning.cbit.com.cn/www/views/checking.jsp?dt=' + urllib.parse.quote(
            ' ' + time.strftime(
                "%a %b %d %Y %H:%M:%S")) + '%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'
        login_url = 'https://learning.cbit.com.cn/www//login/userlogin.do'

        # 获取验证码，并ORC
        self.logger.debug("尝试获取验证码")
        response = RT.get(url=verification_code_url, headers=self.headers)
        verification_code = OCRreader.readtext(response.content, detail=0)[0]
        self.logger.debug(f"验证码为{verification_code}")
        sessionID = dict(response.headers)['Set-Cookie'].split(', ')[-1].split('=')[-1]
        AlteonP = dict(response.headers)['Set-Cookie'].split('; ')[0].split('=')[-1]
        JSESSIONID = dict(response.headers)['Set-Cookie'].split('; ')[1].split('=')[-1]

        self.headers['sessionID'] = sessionID
        # 登录
        en_name = encryption.encrypt(self.name).decode()
        en_passwd = encryption.encrypt(self.passwrd).decode()
        self.logger.debug(f"en_name: {en_name}\ten_passwd: {en_passwd}")
        # print("passwd: " + self.encryption.encrypt(self.passwd).decode())
        login_data = {'username': en_name, 'password': en_passwd,
                      'yzm': verification_code,
                      'convHtmlField': 'username,password', 'loginType': 'pcLogin', 'sessionID': sessionID}
        response = RT.post(data=login_data, url=login_url, headers=self.headers)
        token = dict(response.json())['token']
        self.logger.debug(f"登录成功,token={token}")
        self.headers['token'] = token
        self.headers["Cookie"] = f'AlteonP={AlteonP}; JSESSIONID={JSESSIONID}'
        self.logger.info(f'{self.name} 登录成功')

    def get_lessons_id(self) -> dict:
        self.logger.debug('获得lessons id')
        base_url = "https://learning.cbit.com.cn/www/onlineTraining/trainingdetails.do?"
        data = {"id": self.tcid}
        url = base_url + urlencode(data)
        result = dict(RT.get(url=url, headers=self.headers).json())
        self.logger.debug(result)

        # for i in range(10):
        #     if result is None or result.get('traininglesson') is None:
        #         result = rt.get(url=url)
        #     else:
        #         break
        return result["traininglesson"]

    def get_item_id(self, lessonID) -> dict:
        base_url = "https://learning.cbit.com.cn/www//lessonDetails/details.do"
        data = {"tcid": self.tcid, "lessonId": lessonID}
        #  url = base_url + urlencode(data)
        for i in range(5):
            result = dict(RT.post(data, url=base_url, headers=self.headers).json())
        return result["lessonitem"]

    def post_schedule(self, lessonId, itemId, tcid, totalTime, studyplan=0):
        base_url = (
            "https://learning.cbit.com.cn/www/lessonDetails/updateLessonProcessPC.do?"
        )
        studytime = totalTime * studyplan / 100
        while totalTime > studytime:
            self.logger.info(f"{self.name}: 已经学习了{str(studytime)}秒，还剩{str(totalTime - studytime)}秒")
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
            for i in range(3):
                result = RT.post(url=url, data=data, headers=self.headers)

    def learn(self):
        # 获得lessonID
        self.login()
        lessonsID = self.get_lessons_id()
        for lessonID in lessonsID:
            lession_infomation = self.get_item_id(lessonID["id"])
            for li in lession_infomation:
                if li["studyplan"] == 100:
                    self.logger.info(f"{self.name}: 已经学过了：{li['itemname']}，自动跳过。")
                    continue
                self.logger.info(f"{self.name}: 开始学习{li['itemname']}")
                self.post_schedule(
                    lessonID["id"],
                    li["id"],
                    self.tcid,
                    li["all_times"],
                    li["studyplan"],
                )


def learn_task(user_info):
    lc = Learn_Cbit(name=user_info['name'],
                    passwrd=user_info['passwd'], tcid=user_info['tcid'], speed=1.5)
    lc.learn()


if __name__ == "__main__":
    file_path = 'D:\\Twikura\\token.json'
    with open(file_path, 'r') as file:
        users = json.load(file)
    # max_threads = len(users)
    # with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    #     for u in users:
    #         executor.submit(learn_task, u)
    for u in users:
        learn_task(u)

