import requests
import random
import datetime
import time
import json

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
]


def test(proxy=None):
    try:
        response = requests.get(
            'https://maimai.cn/contact/interest_contact/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1IjoxMTk4MjA4NDAsImxldmVsIjoyLCJ0IjoiY3R0In0.fnz6vNCb63n2j-Frr6H_vu1LuG1jgfoq2oPOITSAJdA',
            proxies=proxy,
            timeout=5,
            headers={'User-Agent': random.choice(USER_AGENTS), })
        print(json.loads(response.text))
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    PROXY_POOLS = ['https://113.200.56.13:8010', 'https://114.91.164.97:9999', 'https://221.6.201.18:9999',
                   'https://202.112.237.102:3128', 'https://140.143.96.216:80', 'https://122.227.62.66:55816']
    res = []
    for i in PROXY_POOLS:
        print(i)
        if test(proxy={'https': i}):
            res.append(i)
    print(res)
