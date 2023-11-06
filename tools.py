def str_to_headers(str):
    for ss in str.strip().split('\n'):
        s = ss.split(':')
        print(f"'{s[0].strip()}': '{s[1].strip()}',")


if __name__ == '__main__':
    str = '''
        Connection: keep-alive
        Pragma: no-cache
        Cache-Control: no-cache
        sec-ch-ua: "Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"
        sec-ch-ua-mobile: ?0
        sec-ch-ua-platform: "Windows"
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
        Sec-Fetch-Site: none
        Sec-Fetch-Mode: navigate
        Sec-Fetch-User: ?1
        Sec-Fetch-Dest: document
        Accept-Encoding: gzip, deflate, br
        Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5

    '''
    print(str_to_headers(str))
