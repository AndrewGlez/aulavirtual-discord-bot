import json
from bs4 import BeautifulSoup
import requests
import re

def get_page(MoodleSession, url):
    cookies = {
        'MoodleSession': f'{MoodleSession}',
    }

    headers = {
        'authority': 'moodle.pucese.edu.ec',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'es-ES,es;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'MoodleSession=rqth1g58ash9o2m1vkmgkl7n4r',
        'referer': 'https://moodle.pucese.edu.ec/my/',
        'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }

    response = requests.get(f'{url}', cookies=cookies, headers=headers, verify=False)

    soup = BeautifulSoup(response.content, 'html.parser')
    
    box = None
    links = None
    try:
        box = soup.find('div', class_='inteconte')
        box = box.text.strip()
        box = (re.sub(r"\s{2,}", "\n", box))
    except:
        raise Exception("Could not format data in source page")
    
    try:
        links = soup.find('iframe')
        links = links['src']
    except:
        links = ''
    return box, links
    




#get_page('rqth1g58ash9o2m1vkmgkl7n4r', 19030)


