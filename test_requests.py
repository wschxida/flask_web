
import requests

url = "https://www.sohu.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Connection": "keep - alive",
}

url = url.replace('http://','')
url = url.replace('https://','')
print(url)

# response = requests.get(url, headers=headers)
# response.encoding = "utf-8"
# text = response.text
#
# print(text)