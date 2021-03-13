from pandas.core.common import SettingWithCopyWarning
import warnings
from selenium import webdriver

import time
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
import urllib.request as req

import requests
import psycopg2
from dotenv import load_dotenv
import os
import glob
import datetime
import re

load_dotenv()
address = os.environ["MY_ADRESS"]
password = os.environ["MY_PASS"]

options = webdriver.ChromeOptions()
headers = {"User-Agent": "Mozilla/5.0"}
prefs = {"download.default_directory": "C:\\Users\\sasno\\Desktop\\Mypandas\\vleague"}
options.add_experimental_option("prefs", prefs)
options.add_argument("--headless")

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

# GoogleChromeを起動
browser = webdriver.Chrome(
    executable_path='C:\\Users\\sasno\\anaconda3\\lib\\site-packages\\chromedriver_binary\\chromedriver.exe', options=options)
browser.implicitly_wait(3)

# ログインするサイトへアクセス
url_login = "https://vleague.tv/signin"
browser.get(url_login)
time.sleep(3)
print("ログインページにアクセスしました")

# テキストボックス入力
element = browser.find_element_by_id('account-mail')
# element.clear()
element.send_keys(address)
element = browser.find_element_by_id('account-pw')
# element.clear()
element.send_keys(password)
print("フォームを送信")
# 入力したデータをクリック
browser_from = browser.find_element_by_class_name('btn_submit')
time.sleep(1)
browser_from.click()
print("情報を入力してログインボタンを押しました")
# ログインするサイトへアクセス
time.sleep(1)
url_login = 'https://vleague.tv/match'
browser.get(url_login)
time.sleep(3)
print("ログインページにアクセスしました")


os.chdir('C:\\Users\\sasno\\Desktop\\MyPandas\\vleague')
# division = 'v1_m'
# division = 'v2_m'
# division = 'v3_m'
# division = 'v2_w'
s_round = '2020-21_regular'
s_round = '2020-21_playoff'
s_round = '2021_Vcup'
division = 'v1_w'
# s_round = '2020-21_Vcup'
# game_set = 1
os.chdir('{}'.format(division))
print(os.getcwd())
# Scheduleからライブスコアを取得
# for文で回す
# 試合

# csvs:list


def remove_csv(csvs):
    judge = False
    for csv in csvs:
        if os.path.exists(csv):
            os.remove(csv)
            judge = True
    if judge:
        print('既存のcsvを削除')


def click(path):
    element = browser.find_element_by_xpath(path)
    browser.implicitly_wait(3)
    element.click()
    time.sleep(1)


text = ''


def create_csv():
    browser.get(url_login)
    time.sleep(1)
    # v1_m:1
    # v1_w:4
    element = browser.find_element_by_xpath(
        '//*[@id="schedule"]/div/div[1]/ul/li[4]')
    browser.implicitly_wait(3)
    element.click()
    time.sleep(1)
    element.click()

    daily = browser.find_element_by_xpath(
        '//*[@id="schedule"]/div/div[3]/div[{}]/div[2]/p[1]'.format(game_num)).text
    daily = daily.replace('.', '-')[:10]
    click('//*[@id="schedule"]/div/div[3]/div[{}]/p/a'.format(game_num))
    click('//*[@id="livescore"]/div[3]/div[1]/ul/li[2]')
    team = browser.find_elements_by_class_name('team_name')
    h_team = team[0].text
    a_team = team[1].text
    print(game_num, daily, h_team, a_team)
    game_sets = browser.find_element_by_class_name('history_set').text

    for game_set in range(1, game_sets.count('\n')+2):
        #         for game_set in range(2, 3):
        count = 0
        home_game_log = pd.DataFrame()
        while len(home_game_log) < 10 or count < 3:

            browser.execute_script("window.scrollTo(0, 0)")
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            browser.implicitly_wait(3)
            element = browser.find_element_by_xpath(
                '//*[@id="livescore"]/div[3]/div[2]/ul/li[{}]'.format(game_set))
            browser.implicitly_wait(3)
            element.click()
#             print(game_set)
            time.sleep(3)
            element.click()
            historys = browser.find_elements_by_class_name('history_item')
            # print(len(historys))
            log_len = len(historys)
            text = ""

            log_lists = []
            home_p = 0
            away_p = 0
#             print(log_len)
            try:
                count += 1
                log_df = pd.DataFrame()
                home_game_log = pd.DataFrame()
                away_game_log = pd.DataFrame()
                for i in range(1, log_len+1):
                    #                     //*[@id="livescore"]/div[3]/div[2]/div/div[1]/div[1]
                    home_history = browser.find_element_by_xpath(
                        '//*[@id="livescore"]/div[3]/div[2]/div/div[{}]/div[1]'.format(str(i))).text
                #     print(home_history)
                    home_point = browser.find_element_by_xpath(
                        '//*[@id="livescore"]/div[3]/div[2]/div/div[{}]/div[2]'.format(str(i))).text
                    if home_point == '':
                        home_point = home_p
                    else:
                        home_p = int(home_point)
                    away_history = browser.find_element_by_xpath(
                        '//*[@id="livescore"]/div[3]/div[2]/div/div[{}]/div[5]'.format(str(i))).text
                    away_point = browser.find_element_by_xpath(
                        '//*[@id="livescore"]/div[3]/div[2]/div/div[{}]/div[4]'.format(str(i))).text
                    if away_point == '':
                        away_point = away_p
                    else:
                        away_p = int(away_point)
                #     print(home_point, away_point)
                    log_list = [home_p, away_p, home_history, away_history]
                #     print(log_list)
                    log_lists.append(log_list)
                log_df = pd.DataFrame(data=log_lists)

#             print(log_lists[-1])
                home_log = log_df[2].str.split(expand=True)
                home_log = home_log.mask(
                    home_log.loc[:, 2].isnull() == True, home_log.shift(axis=1))
                # print(len(home_log.columns))
                if len(home_log.columns) == 3:
                    home_log[["交代番号", "交代選手"]] = None
                home_log.columns = ["状況", "番号", "選手", "交代番号", "交代選手"]
                # home_log
                away_log = log_df.loc[:, 3].str.split(expand=True)
                away_log = away_log.mask(
                    away_log.loc[:, 2].isnull() == True, away_log.shift(axis=1))
                # print(len(away_log.columns))
                if len(away_log.columns) == 3:
                    away_log[["相手交代番号", "相手交代選手"]] = None
                away_log.columns = ["相手状況", "相手番号", "相手選手", "相手交代番号", "相手交代選手"]
                # away_log
                point = log_df[[0, 1]]
                point.columns = ["得点", "失点"]
                # SettingWithCopyWarning: 後から修正
                point['+/-'] = point["得点"] - point["失点"]

                def f(x): return 'Lead' if x > 0 else (
                    'Tie' if x == 0 else 'Behind')
                point['L-B'] = point['+/-'].map(f)
                # point
                away_point = point.reindex(["失点", "得点", '+/-', 'L-B'], axis=1)
                away_point['+/-'] = away_point['+/-'].map(lambda x: -x)
                away_point['L-B'] = away_point['+/-'].map(f)
                away_point.columns = ["得点", "失点", '+/-', 'L-B']
                # away_point
                home_game_log = pd.concat([point, home_log, away_log], axis=1)
                away_game_log = pd.concat(
                    [away_point, away_log, home_log], axis=1)
                away_game_log.columns = home_game_log.columns
            except:
                count += 1
                print('error_1')
                pass

        if count >= 3:
            text += '{}-{}set\n'.format(game_num, game_set)

        home_csv = '{}/{}/{}-livescore-{}set.csv'.format(
            h_team, s_round, daily, game_set)
        away_csv = '{}/{}/{}-livescore-{}set.csv'.format(
            a_team, s_round, daily, game_set)
        home_csv_2 = 'all/{}/{}-livescore-{}vs{}-{}set.csv'.format(
            s_round, daily, h_team, a_team, game_set)
        away_csv_2 = 'all/{}/{}-livescore-{}vs{}-{}set.csv'.format(
            s_round, daily, a_team, h_team, game_set)
        # remove_csv([home_csv, away_csv, home_csv_2, away_csv_2])

        if(len(home_game_log) > 10):
            home_game_log.to_csv(home_csv, index=False)
            away_game_log.to_csv(away_csv, index=False)
            home_game_log.to_csv(home_csv_2, index=False)
            away_game_log.to_csv(away_csv_2, index=False)
            print('{}セット目csv作成成功'.format(game_set))
        else:
            print('データ無し')
        time.sleep(1)


# v1_m
# 3/7 141~145
# v1_w
# 3/6 142~147
# 3/7 148~151
# //*[@id="schedule"]/div/div[3]/div[118]/p/a
for game_num in range(118, 119):
    try:
        create_csv()
    except:
        print('error_2 and retry')
        text += '{}\n'.format(game_num)
        time.sleep(1)
        create_csv()
        pass
print(text)

browser.close()
