import requests
import time
import sys
import random
import argparse
import re
from bs4 import BeautifulSoup

def clean_text(text):
    text = re.sub(r'Chapter\s+Text', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

parser = argparse.ArgumentParser(description='AO3文章下载工具')
parser.add_argument('--url', help='AO3文章网址')
parser.add_argument('--proxy', help='HTTP代理地址，例如: http://127.0.0.1:11451')

args = parser.parse_args()

if args.url:
    url = args.url.strip()
else:
    url = input("请输入ao3文章网址：").strip()

if '/chapters/' in url:
    url = url.split('/chapters/')[0]

# 默认代理配置（如需使用请取消注释）
# proxies = {
#     "http": "http://127.0.0.1:11451",
#     "https": "http://127.0.0.1:11451"
# }

proxies = None
if args.proxy:
    proxies = {
        "http": args.proxy,
        "https": args.proxy
    }

if 'view_full_work' not in url:
    if '?' in url:
        url += '&view_full_work=true'
    else:
        url += '?view_full_work=true'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

try:
    response = requests.get(url, proxies=proxies, timeout=30, headers=headers)
except Exception as e:
    print(f"请求失败: {e}")
    sys.exit(1)

if response.status_code == 429:
    print("请求太频繁了，让我小睡一会Zzz")
    sleeptime = random.randint(60, 90)
    time.sleep(sleeptime)
    print("睡醒了，又充满活力啦！")
    sys.exit()

if response.status_code != 200:
    print(f"页面请求失败，状态码: {response.status_code}")
    sys.exit(1)

soup = BeautifulSoup(response.text, "html.parser")

title_elem = soup.find("h2", class_="title")
if not title_elem:
    print("无法找到文章标题，可能页面结构变化或请求被拦截")
    sys.exit(1)

title = title_elem.text.strip()
title = title.replace('\n', '').replace('/', '').replace('  ', ' ').replace('|', '').replace(':', '').replace('<', '').replace('>', '').replace('?', '').replace('*', '').replace('\\', '')

author_elem = soup.find("a", rel="author")
if author_elem:
    author = author_elem.text.strip()
else:
    author_elem = soup.find("h3", class_="author")
    author = author_elem.text.strip() if author_elem else "未知作者"

chapters = soup.find_all('div', id=lambda x: x and x.startswith('chapter-'))

with open(f"{title}-{author}.txt", 'w', encoding='utf-8') as f:
    if chapters:
        for chapter in chapters:
            chapter_title = chapter.find('h3', class_='title')
            if chapter_title:
                f.write(chapter_title.text.strip() + '\n')
            content = chapter.find("div", class_="userstuff")
            if content:
                for elem in content.find_all(['h3', 'h4'], class_='landmark'):
                    elem.decompose()
                text = content.get_text(separator='\n', strip=True)
            else:
                text = chapter.get_text(separator='\n', strip=True)
            text = re.sub(r'Chapter\s+Text', '', text, flags=re.IGNORECASE)
            lines = [l.strip() for l in text.split('\n') if l.strip() and 'Chapter Text' not in l]
            f.write('\n'.join(lines) + '\n\n')
    else:
        content = soup.find("div", class_="userstuff")
        if content:
            for landmark in content.find_all(class_='landmark'):
                landmark.decompose()
            f.write(title + '\n')
            f.write('作者：' + author + '\n\n')
            text = clean_text(content.text)
            lines = [line for line in text.split('\n') if 'Chapter Text' not in line]
            text = '\n'.join(lines)
            f.write(text + '\n')
        else:
            print("未找到文章内容")
            sys.exit(1)

print(f"好耶！爬取成功！标题：{title}，作者：{author}，章节数：{len(chapters) if chapters else 1}")
