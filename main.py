import concurrent
import json
from Learn_Cbit import Learn_Cbit


def learn_task(user_info):
    lc = Learn_Cbit(phone=user_info['phone'], name=user_info['name'],
                    passwrd=user_info['passwd'], tcid=user_info['tcid'])
    lc.learn()


if __name__ == "__main__":
    file_path = 'D:\\Twikura\\token.json'
    with open(file_path, 'r',encoding='utf-8') as file:
        users = json.load(file)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for u in users:
            executor.submit(learn_task, u)
    # for u in users:
    #     learn_task(u)
