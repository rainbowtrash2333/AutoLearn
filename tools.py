from typing import Dict, Optional


def str_to_headers(header_str: str) -> None:
    """Convert header string to dictionary format for easy copying
    
    Args:
        header_str: Multi-line string containing HTTP headers
    """
    for line in header_str.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            print(f"'{key.strip()}': '{value.strip()}',")


if __name__ == '__main__':
    sample_headers = '''
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
    str_to_headers(sample_headers)
