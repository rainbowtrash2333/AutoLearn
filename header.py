from pprint import pprint

def gen_header_from_str():
    str = '''
    Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5
Connection: keep-alive
Cookie: AlteonP=0a140c030aff050621dda83d1b13; JSESSIONID=fItGQliR1I9CGEWAzFwYfIqM2t7IEeYld4YbTPhwPUG1kXKKN-_7!874735712
Host: learning.cbit.com.cn
Referer: https://learning.cbit.com.cn/www/views/trainingclass/trainingDetails.html?tcid=e491bf3476e64fe19f61e472c7a41480
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0
X-Requested-With: XMLHttpRequest
apikey: 2456269a445b4a18afad29fd12714da2
isapp: 0
sec-ch-ua: "Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
token: eyJ0eXAiOiJKV1QiLCJ0eXBlIjoiSldUIiwiZW5jcnlwdGlvbiI6IkhTMjU2IiwiYWxnIjoiSFMyNTYifQ.eyJUaW1lIjoxNjg0ODA1OTMzMDU3LCJleHAiOjE2ODQ4OTIzMzMsInVzZXJJZCI6IjNkY2U4ZmUxMWU0ZjRmMjdiYTJlNTViMTIzZTkzOWU2IiwidXNlckNvZGUiOiIxOTE4NDIzNjI0NCJ9.MUOu-UsM0LFh7J1K9M31Z3bLI3aNtdnJODvEhIVjRqM
'''
    header={}
    substrs = str.strip().split("\n")
    for s in substrs:
        ss= s.strip() .split(':')
        header[ss[0].strip()]=ss[1].strip()
    return header
if __name__ == '__main__':
    print(gen_header_from_str())