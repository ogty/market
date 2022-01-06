import datetime
import json
import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import tweepy

from src.download_update import download_update
import settings


load_dotenv()
oldest_month = 0
ALL_COMPANIES = 0

client = tweepy.Client(
    os.environ["BEARER_TOKEN"], 
    os.environ["API_KEY"], 
    os.environ["API_KEY_SECRET"], 
    os.environ["ACCESS_TOKEN"], 
    os.environ["ACCESS_TOKEN_SECRET"]
)

def logger(message: str) -> None:
    now = datetime.datetime.now()
    log = f"{now} | {message}"
    print(log)

    if not os.path.exists(settings.LOGS_DIR):
        os.makedirs(settings.LOGS_DIR)
        
    this_year_month = datetime.datetime.now().strftime("%Y_%m")
    with open(os.path.join(settings.LOGS_DIR, f"{this_year_month}.log"), "a", encoding="utf-8") as f:
        f.write(f"{log}\n")

def trend() -> None:
    global ALL_COMPANIES
    global oldest_month 

    latest_month = datetime.datetime.now().month

    if latest_month != oldest_month:
        ALL_COMPANIES = download_update()
        oldest_month = latest_month

    url = "https://info.finance.yahoo.co.jp/ranking/?kd=1&tm=d&mk=1"
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    data = soup.select("[class='rankdataPageing yjS']")
    result = data[0].text
    up_companies = result.split("/")[1].replace("件中", "")
    
    up_rate = int(up_companies) / ALL_COMPANIES
    down_rate = str(round((1.0 - up_rate) * 100, 3)).ljust(6)
    up_rate = str(round(up_rate * 100, 3)).ljust(6)

    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    message = f"{up_rate} | {down_rate}"
    twitter_message = f"{now}\n　UP　：{up_rate}%\nDOWN：{down_rate}%"

    logger(message)
    
    # Twitter bot
    client.create_tweet(text=twitter_message)

    # Slack bot
    requests.post(
        os.environ["WEB_HOOK_URL"], 
        data=json.dumps({
            "text" : message,
            "icon_emoji" : ":dog:",
            "username" : "Trend"
            }
        )
    )

def market_holidays(year: str, path: str) -> None:
    url = "https://www.jpx.co.jp/corporate/about-jpx/calendar/index.html"
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    data = soup.select("[class='a-center']")
    holidays = [data[i].text for i in range(len(data)) if i % 2 == 0]

    holidays = list(filter(lambda x: x.startswith(year), holidays))
    holidays = list(map(lambda x: x[:-3], holidays))

    with open(path, "w", encoding="utf-8") as f:
        for holiday in holidays:
            f.write(f"{holiday}\n")

def is_open() -> bool:
    year = str(datetime.datetime.now().year)
    
    path = os.path.join(settings.DATA_DIR, f"{year}.txt")
    if not os.path.exists(path):
        market_holidays(year, path)
    
    with open(path, "r", encoding="utf-8") as f:
        holidays = [holiday.rstrip() for holiday in f]

    weekday = datetime.datetime.now().weekday()
    now = datetime.datetime.now().strftime("%Y/%m/%d")

    if weekday < 5:
        if not now in holidays:
            return True
        else:
            return False
    else:
        return False