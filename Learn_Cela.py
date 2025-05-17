import json
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
import re
from datetime import datetime

COOKIE = "SESSION=; acw_tc="

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Cookie": COOKIE,
    "Host": "cela.gwypx.com.cn",
    "Origin": "https://cela.gwypx.com.cn",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "X-KL-Ajax-Request": "Ajax_Request",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}


def get_courses(unitId: int) -> json:
    url = "https://cela.gwypx.com.cn/portal/serarch_course_list.do"
    "unitId=1233&showStyle=hengpai&courseYear="
    data = {
        "unitId": unitId,
        "showStyle": "hengpai",
        "courseYear": ""
    }
    courseStr = dict(RT.post(url=url, data=data, headers=headers).json())
    courses = json.loads(courseStr["courseStr"])
    return courses


def get_course_time(courseId: int) -> int:
    import requests
    url = f'https://cela.gwypx.com.cn/portal/course_detail.do?courseId={courseId}'
    # response = requests.get(url,headers=headers)
    response = RT.get(url=url, headers=headers)
    matches = re.findall(r'(\d+)\s*分钟', response.text)
    # 如果有多个匹配，取第一个
    if matches:
        return (int(matches[0]) + 1) * 60
    # print(response.text)
    return 0


def get_user_id(user_course_id: str) -> str:
    url_player = rf"https://cela.gwypx.com.cn/portal/playcourse.do?rate_play=&id=118186420&type=1&play_sco=null&year="
    response = RT.get(url=url_player, headers=headers)
    match = re.search(r'user_id\s*=\s*"(\d+)"', response.text)
    if match:
        return match.group(1)
    print(response.text)
    exit(0)
    return ""


def get_process(courseId: int) -> float:
    url = f"https://cela.gwypx.com.cn/portal/course_detail.do?courseId={courseId}"
    response = RT.get(url=url, headers=headers)
    match = re.search(r'>(\d+(?:\.\d+)?)%', response.text)
    if match:
        process = float(match.group(1))
        return process
    print(response.text)
    exit(0)
    return 0


def post_schedule(userid: str, user_course_id: str, courseId: int, time: int):
    url = f"https://cela.gwypx.com.cn/device/study_sync.do?user_id={userid}"
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    params = {
        "study_sync": {"user_id": userid,
                       "course_sync": [{"user_course_id": f"{user_course_id}", "course_id": f"{courseId}",
                                        "scorm_data": [
                                            {"sco_id": "res01", "lesson_location": f"{time}.0",
                                             "session_time": 30,
                                             "last_learn_time": formatted_time}]}]}}
    encoded_data = json.dumps(params)
    data = {"data": encoded_data}
    response = RT.post(url=url, data=data, headers=headers).json()
    if response["message"] != "操作成功":
        print(f"{courseId}异常")
        print(response)


def select_course(courseId: int):
    url = "https://cela.gwypx.com.cn/student/course_select.do"
    data = {"courseId": courseId}

    response = RT.post(url=url, data=data, headers=headers).json()


def __test():
    courses = get_courses(1234)
    for course in courses:
        print(f"开始课程：{course['course_name']} ")
        if "process" in course and float(course["process"]) == 100:
            print(f"{course['course_name']} 已完成")
            continue
        courseId = int(course["id"])
        select_course(courseId=courseId)
        time = get_course_time(courseId=courseId)
        user_id = get_user_id(user_course_id=course['usercourseid'])
        while get_process(courseId) < 100:
            post_schedule(userid=user_id, user_course_id=course['usercourseid'], courseId=courseId, time=time)
        print(f"{course['course_name']} 已完成")


if __name__ == '__main__':
    raise SystemExit(__test())
