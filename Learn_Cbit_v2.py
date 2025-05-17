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


class Learn_Cbit:

    # phone 登录名，一般为电话号码
    # tcid 课程id
    # passwd 登录密码
    # speed 刷课速度，默认为1.5倍数
    # level filename filemode  日志系统参数
    def __init__(self, phone, name, lessonLibrary_id, password='123456') -> None:
        config = Config.get_config()
        self.phone = phone
        self.password = password
        self.lessonLibrary_id = lessonLibrary_id
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

    def __login(self):
        OCRreader = easyocr.Reader(['ch_sim'])
        encryption = AESCipher('dacf107e4bdbbef0', 'bcancid682e09aec')
        self.logger.info(f"{self.name}尝试登录")
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
            en_passwd = encryption.encrypt(self.password).decode()
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

    def __get_lessons_id(self) -> list[str]:
        base_url = "https://learning.cbit.com.cn/www/lesson/selectLessonApp.do"
        data = {"leName": "", "keyword": "", "pageSize": 9999, "sort": "createtime",
                "id": self.lessonLibrary_id, "level": 5, "pagetitle": "lessonLibrary"}
        response = RT.post(url=base_url, data=data, headers=self.headers)
        result = dict(response.json())
        self.logger.debug(f"__get_lessons->response: {result}")
        lesson_id_list = [lesson["id"] for lesson in result["lessonList"]]

        return lesson_id_list

    def __get_lesson_items_id(self, lessonID: str) -> list[dict[str, str]] | None:
        base_url = "https://learning.cbit.com.cn/www//lessonDetails/details.do"
        data = {"lessonId": lessonID}
        result = {}
        for i in range(self.retry):
            response = RT.post(url=base_url, data=data, headers=self.headers)
            if len(response.text) > 6:
                result = dict(response.json())
                if 'lessonitem' in result:
                    result = [
                        {"id": lesson_item["id"], "time": lesson_item["all_times"],
                         "name": lesson_item["itemname"]}
                        for lesson_item in
                        result["lessonitem"]]

                    self.logger.debug(f"__get_lesson_items_id->result:{result}")
                    return result

    def __post_schedule(self, lessonId: str, itemId: str, totalTime: float, lesson_name: str, studyplan=0):
        base_url = (
            "https://learning.cbit.com.cn/www/lessonDetails/updateLessonProcessPC.do?"
        )
        data = {
            "lessonId": lessonId,
            "lessonItemId": itemId,
            "process": "-2",
            "tcid": 'null',
            "totalTime": totalTime,
        }
        if self.mode == 'fast':
            data["suspendTime"] = totalTime
            data["studytime"] = totalTime
            url = base_url + urlencode(data)
            for i in range(self.retry):
                response = dict(RT.post(url=url, data=data, headers=self.headers).json())
                if response['success']:
                    self.logger.debug(f"__post_schedule->response: {response}")
                    self.logger.info(f"{self.name}: 已经学习{lesson_name}。")
                    break
            else:
                self.logger.error(f"{self.name}: 课程{lesson_name}失败。")
                self.logger.error(f"data:{data}\nheader={self.headers}")

        if self.mode == 'normal':
            studytime = totalTime * studyplan / 100
            while totalTime > studytime:
                self.logger.info(
                    f"{self.name}: 已经学习{lesson_name} {str(studytime)}秒，还剩{str(totalTime - studytime)}秒")
                random_num = random.randint(20, 80) // self.speed
                time.sleep(random_num)
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
        self.__login()
        lesson_id_list = self.__get_lessons_id()
        if len(lesson_id_list) == 0:
            self.logger.error(f"{self.name}未发现课程，请检查课程id")
            return 0
        for lesson_id in lesson_id_list:
            lesson_item_list = self.__get_lesson_items_id(lesson_id)
            for lesson_item in lesson_item_list:
                self.__post_schedule(lessonId=lesson_id, itemId=lesson_item["id"], totalTime=float(lesson_item["time"]),
                                     lesson_name=lesson_item["name"])


def learn_task(user_info):
    lc = Learn_Cbit(phone=user_info['phone'], name=user_info['name'],
                    password=user_info['passwd'], lessonLibrary_id=user_info['tcid'])
    lc.learn()


def __test():
    import json

    file_path = 'D:\\Twikura\\token.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        users = json.load(file)
        learn_task(users[1])


if __name__ == '__main__':
    raise SystemExit(__test())
