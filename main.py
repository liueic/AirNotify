import requests
import os
import json

bark_key = os.environ['BARK_KEY']
air_key = os.environ['AIR_PUBLIC_KEY']

# 这里的 city 需从 aqicn 获取对应城市代码，例如北京
# city = os.environ['CITY']
bark_api = "https://api.day.app/" + bark_key
air_api = "https://api.waqi.info/feed/@1451/?token=" + air_key


def push_announce(title, message):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
    }
    body = {
        "body": message,
        "title": title,
        "badge": 1,
        "sound": "minuet",
        "icon": "https://aqicn.org/images/logo/regular.png",
        "group": "Weather",
    }
    try:
        requests.post(bark_api, headers=headers, data=json.dumps(body))
    except requests.exceptions.RequestException as e:
        print("通知发送失败：", e)


def get_data():
    response = requests.get(air_api)
    data = response.json()
    # 假设返回数据格式为 {'data': {'aqi': 数值, 'iaqi': { ... } } }
    aqi = data['data']['aqi']
    iaqi_values = {key: value["v"] for key, value in data["data"]["iaqi"].items()}
    return aqi, iaqi_values


def analyze(aqi):
    if aqi <= 50:
        return 1  # 优
    elif aqi <= 100:
        return 2  # 良
    elif aqi <= 150:
        return 3  # 轻度污染
    elif aqi <= 200:
        return 4  # 中度污染
    elif aqi <= 250:
        return 5  # 重度污染
    else:
        return 6  # 严重污染


if __name__ == '__main__':
    aqi, iaqi_values = get_data()
    quality = analyze(aqi)

    # 根据空气质量级别发送不同的提醒
    if quality == 2:
        push_announce("天气提醒", f"当前空气质量为良，请注意天气变化，当前AQI为：{aqi}")
    elif quality in [3, 4]:
        push_announce("健康提醒", f"当前空气质量为轻度或中度污染，出门请佩戴口罩，当前AQI为：{aqi}")
    elif quality in [5, 6]:
        push_announce("出行建议", f"当前空气质量为重度或严重污染，建议尽量不要外出，当前AQI为：{aqi}")
    else:
        print("空气质量优，无需提醒。")