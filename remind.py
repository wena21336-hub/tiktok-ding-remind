import requests
from datetime import datetime, timedelta
import os

DING_WEBHOOK = os.getenv("DING_WEBHOOK")

def send_ding(title, content):
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "markdown",
        "markdown": {"title": title, "text": content}
    }
    requests.post(DING_WEBHOOK, json=data, headers=headers)

def is_europe_dst(now):
    year = now.year
    march_last = datetime(year, 3, 31)
    march_last -= timedelta(days=march_last.weekday()+1)
    oct_last = datetime(year, 10, 31)
    oct_last -= timedelta(days=oct_last.weekday()+1)
    return march_last <= now < oct_last

def is_mexico_dst(now):
    year = now.year
    march_second = datetime(year,3,1)
    while march_second.weekday() != 6:
        march_second += timedelta(days=1)
    march_second += timedelta(days=7)
    nov_first = datetime(year,11,1)
    while nov_first.weekday() != 6:
        nov_first += timedelta(days=1)
    return march_second <= now < nov_first

def get_remind_time():
    now = datetime.now()
    eu_dst = is_europe_dst(now)
    mx_dst = is_mexico_dst(now)
    uk_remind = "02:30" if eu_dst else "01:30"
    eu5_remind = "03:30" if eu_dst else "02:30"
    mx_remind = "06:30" if mx_dst else "07:30"
    return uk_remind, eu5_remind, mx_remind, eu_dst, mx_dst

def remind_uk():
    send_ding("⏰ 英国投放提醒", """
【TikTok 英国黄金时段开启提醒】
本地18:00–24:00流量高峰
请开启计划、放开预算、盯消耗！
""")

def remind_eu5():
    send_ding("⏰ 欧洲5国投放提醒", """
【TikTok 德/法/匈/波/捷 黄金时段开启提醒】
本地18:00–24:00流量高峰
请开启计划、放开预算、盯消耗！
""")

def remind_mx():
    send_ding("⏰ 墨西哥投放提醒", """
【TikTok 墨西哥黄金时段开启提醒】
本地18:00–24:00流量高峰
请开启计划、放开预算、盯消耗！
""")

def daily_summary():
    uk_t, eu5_t, mx_t, eu_dst, mx_dst = get_remind_time()
    dst_text = "【夏令时生效】" if eu_dst else "【冬令时生效】"
    send_ding("📊 TikTok全域投放时段日报", f"""
{dst_text}
今日7国黄金投放提醒时间：
✅ 英国：北京时间 {uk_t} 提醒
✅ 德/法/匈/波/捷：北京时间 {eu5_t} 提醒
✅ 墨西哥：北京时间 {mx_t} 提醒
💡流量高峰：当地 18:00–24:00
""")

if __name__ == "__main__":
    import sys
    task = sys.argv[1] if len(sys.argv)>1 else ""
    if task == "uk": remind_uk()
    elif task == "eu5": remind_eu5()
    elif task == "mx": remind_mx()
    elif task == "daily": daily_summary()
