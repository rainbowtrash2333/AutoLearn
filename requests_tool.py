import requests
from urllib.parse import urlencode

repeat_times = 5  # 重复5次


class Non200Error(Exception):
    def __init__(self, message):
        self.message = message


default_headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0",
    "X-Requested-With": "XMLHttpRequest",
    "isapp": "0",
    "sec-ch-ua": '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}


# if http status code is not 200, then repeat n times
def repeat_decorator(func, n=repeat_times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            status_code = 0
            for i in range(n):
                response = func(*args, **kwargs)
                status_code = response.status_code
                if status_code == 200:
                    return response
            if status_code != 200:
                raise Non200Error(f'{response.url} http status code is {str(status_code)},  is not 200!')

        return wrapper

    return decorator


@repeat_decorator(repeat_times)
def get(url, headers=default_headers):
    response = requests.get(url, headers=headers)
    return response


@repeat_decorator(repeat_times)
def post(data, url, headers=default_headers):
    response = requests.post(url, data=data, headers=headers)
    return response
