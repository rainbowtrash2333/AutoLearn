from urllib.parse import urlencode
from pprint import pprint
from requests_tool import RequestsTool as RT
import random
import time
import json


class Learn_Cbit:
    def __init__(self, cookie, token, tcid, speed=1.5) -> None:
        self.cookie = cookie
        self.token = token
        self.tcid = tcid
        self.speed = speed  # 1.5倍数
        print("开启" + str(speed) + "倍速")

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
        base_url = "https://learning.cbit.com.cn/www//lessonDetails/details.do?"
        data = {"tcid": self.tcid, "lessonId": lessonID}
        url = base_url + urlencode(data)
        rt = RT(cookie=self.cookie, token=self.token, referer=url)
        result = rt.get(url=url)
        for i in range(10):
            if  result.get('lessonitem') is None or result is None:
                result = rt.get(url=url)
            else:
                break
        return result["lessonitem"]

    def post_schedule(self, lessonId, itemId, tcid, totalTime, studyplan=0):
        base_url = (
            "https://learning.cbit.com.cn/www/lessonDetails/updateLessonProcessPC.do?"
        )
        studytime = totalTime * studyplan / 100
        while totalTime > studytime:
            print(f"已经学习了{str(studytime)}秒，还剩{str(totalTime-studytime)}秒")
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
        for lessonID in lessonsID:
            lession_infomation = self.get_item_id(lessonID["id"])
            for li in lession_infomation:
                if li["studyplan"] == 100:
                    print(f"已经学过了：{li['itemname']}，自动跳过。")
                    continue
                print(f"开始学习{li['itemname']}")
                self.post_schedule(
                    lessonID["id"],
                    li["id"],
                    self.tcid,
                    li["all_times"],
                    li["studyplan"],
                )


if __name__ == "__main__":
    file_path = 'D:\\Twikura\\token.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    lc = Learn_Cbit(
        token=data['token'], cookie=data['cookie'], tcid=data['tcid'], speed=1.5)
    lc.learn()
