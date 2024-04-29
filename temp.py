import requests

if __name__ == '__main__':
    url = "https://api.telegram.org"
    proxies = {
        'http': 'http://192.168.31.152:7890',
        'https': 'http://192.168.31.152:7890',
    }

    response = requests.get(url, proxies=proxies)
    print(response.status_code)
