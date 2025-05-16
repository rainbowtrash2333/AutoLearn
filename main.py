import time

from Learn_Cbit_v2 import Learn_Cbit
import json
from multiprocessing import Pool


def learn_task(user_info):
    lc = Learn_Cbit(phone=user_info['phone'], name=user_info['name'],
                    password=user_info['passwd'], lessonLibrary_id=user_info['tcid'])
    lc.learn()


def __main():
    file_path = 'E:\\Twikura\\token.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        users = json.load(file)
        # for u in users:
            # learn_task(u)
            # time.sleep(3)
    with Pool(processes=len(users)) as pool:
        pool.map(learn_task, users)


if __name__ == "__main__":
    raise SystemExit(__main())
