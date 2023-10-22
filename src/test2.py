import requests

cookies = {
    'MoodleSession': 'llesdtbcpgjt15pj15mcqgu14h',
}

headers = {
    'authority': 'moodle.pucese.edu.ec',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'es-ES,es;q=0.9',
    'content-type': 'application/json',
    # 'cookie': 'MoodleSession=llesdtbcpgjt15pj15mcqgu14h',
    'origin': 'https://moodle.pucese.edu.ec',
    'referer': 'https://moodle.pucese.edu.ec/my/',
    'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'sesskey': 'IsQpuAUlar',
    'info': 'core_calendar_get_action_events_by_timesort',
}

json_data = [
    {
        'index': 0,
        'methodname': 'core_calendar_get_action_events_by_timesort',
        'args': {
            'limitnum': 6,
            'timesortfrom': 1697950800,
            'timesortto': 1698555600,
            'limittononsuspendedevents': True,
        },
    },
]

response = requests.post(
    'https://moodle.pucese.edu.ec/lib/ajax/service.php',
    params=params,
    cookies=cookies,
    headers=headers,
    json=json_data,
    verify=False,
)

print(response.content)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '[{"index":0,"methodname":"core_calendar_get_action_events_by_timesort","args":{"limitnum":6,"timesortfrom":1697950800,"timesortto":1698555600,"limittononsuspendedevents":true}}]'
#response = requests.post(
#    'https://moodle.pucese.edu.ec/lib/ajax/service.php',
#    params=params,
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)