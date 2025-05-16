# 已过期
import urllib.parse
from urllib.parse import urlencode
from AESCipher import AESCipher
import requests_tool as RT
import random
import time
import easyocr
import logging
from yamlUtils import Config
from exceptions import *
import asyncio


class Learn_Cbit:

    # phone 登录名，一般为电话号码
    # tcid 课程id
    # passwd 登录密码
    # speed 刷课速度，默认为1.5倍数
    # level filename filemode  日志系统参数
    def __init__(self, phone, name, tcid, passwrd='123456') -> None:
        config = Config.get_config()
        self.phone = phone
        self.passwrd = passwrd
        self.tcid = tcid
        self.headers = config['headers']
        self.retry = config['Learn_Cbit']['retry']
        self.speed = config['Learn_Cbit']['speed']
        self.mode = config['Learn_Cbit']['mode']
        self.name = name
        self.logging_level = config['logging']['logging_level']
        logging.basicConfig(level=self.logging_level,  # 设置日志级别，可以是DEBUG、INFO、WARNING、ERROR、CRITICAL
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            filename=config['logging']['logging_path'],  # 将日志记录到文件中
                            filemode=config['logging']['logging_mode'],
                            encoding='utf-8')
        console_handler = logging.StreamHandler()  # 创建控制台处理程序
        self.logger = logging.getLogger(phone)
        self.logger.addHandler(console_handler)

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
        login_response = None
        for i in range(self.retry):
            response = RT.get(url=verification_code_url, headers=self.headers)
            verification_code = OCRreader.readtext(response.content, detail=0)[0]
            self.logger.debug(f"验证码为{verification_code}")
            sessionID = dict(response.headers)['Set-Cookie'].split(', ')[-1].split('=')[-1]
            AlteonP = dict(response.headers)['Set-Cookie'].split('; ')[0].split('=')[-1]
            JSESSIONID = dict(response.headers)['Set-Cookie'].split('; ')[1].split('=')[-1]

            self.headers['sessionID'] = sessionID
            # 登录
            en_name = encryption.encrypt(self.phone).decode()
            en_passwd = encryption.encrypt(self.passwrd).decode()
            self.logger.debug(f"en_name: {en_name}\ten_passwd: {en_passwd}")

            login_data = {'username': en_name, 'password': en_passwd,
                          'yzm': verification_code,
                          'convHtmlField': 'username,password', 'loginType': 'pcLogin', 'sessionID': sessionID}
            response = RT.post(data=login_data, url=login_url, headers=self.headers)
            if dict(response.json())['success']:
                login_response = response
                break

        if login_response is not None:
            token = dict(response.json())['token']
            self.logger.debug(f"登录成功,token={token}")
            self.headers['token'] = token
            self.headers["Cookie"] = f'AlteonP={AlteonP}; JSESSIONID={JSESSIONID}'
            self.logger.info(f'{self.name} 登录成功')
        else:
            raise login_failed(f"{self.name} login failed")

    def get_lessons_id(self) -> []:
        self.logger.debug('获得lessons id')
        base_url = "https://learning.cbit.com.cn/www/onlineTraining/trainingdetails.do?"
        data = {"id": self.tcid}
        url = base_url + urlencode(data)
        result = dict(RT.get(url=url, headers=self.headers).json())
        self.logger.debug(result)
        print(f"result:{RT.get(url=url, headers=self.headers).json()}")
        return result["traininglesson"]

    def get_lesson_items_id(self, lessonID) -> str | None:
        base_url = "https://learning.cbit.com.cn/www//lessonDetails/details.do"
        data = {"lessonId": lessonID}
        result = {}
        for i in range(self.retry):
            response = RT.post(data, url=base_url, headers=self.headers)
            if len(response.text) > 6:
                result = dict(response.json())
                if 'lessonitem' in result:
                    return result["lessonitem"]

    def post_schedule(self, lessonId, itemId, tcid, totalTime, studyplan=0):
        base_url = (
            "https://learning.cbit.com.cn/www/lessonDetails/updateLessonProcessPC.do?"
        )
        data = {
            "lessonId": lessonId,
            "lessonItemId": itemId,
            "process": "-2",
            "tcid": tcid,
            "totalTime": totalTime,
        }

        if self.mode == 'fast':
            data["suspendTime"] = totalTime
            data["studytime"] = totalTime
            url = base_url + urlencode(data)
            for i in range(self.retry):
                result = RT.post(url=url, data=data, headers=self.headers)

        if self.mode == 'nomal':
            studytime = totalTime * studyplan / 100
            while totalTime > studytime:
                self.logger.info(f"{self.name}: 已经学习了{str(studytime)}秒，还剩{str(totalTime - studytime)}秒")
                random_num = random.randint(20, 80) // self.speed
                asyncio.sleep(random_num)
                studytime = (
                    studytime + random_num * self.speed
                    if totalTime > studytime + random_num * self.speed
                    else totalTime
                )
                data["suspendTime"] = studytime
                data["studytime"] = studytime
                url = base_url + urlencode(data)
                for i in range(self.retry):
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
                asyncio.run(self.post_schedule(
                    lessonID["id"],
                    li["id"],
                    self.tcid,
                    li["all_times"],
                    li["studyplan"],
                ))
        self.logger.info(f'=========={self.name} 完成所有课程！==========')


def __test():
    import json
    file_path = r'E:/Twikura/token-test.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        users = json.load(file)
    user_info = users[0]
    lc = Learn_Cbit(phone=user_info['phone'], name=user_info['name'],
                    passwrd=user_info['passwd'], tcid=user_info['tcid'])
    lc.learn()


if __name__ == '__main__':
    raise SystemExit(__test())
