import time
import pandas as pd
 

from bs4 import BeautifulSoup
import urllib.request as req

import requests
import os
import datetime
import re
import glob

from team_index import get_teams

now = datetime.datetime.now()

os.chdir('/Users/sasno/Desktop/MyPandas/vleague')

headers = {"User-Agent": "Mozilla/5.0"}

print('ディビジョンを選択してください:{v1_m, v2_m, v3_m, v1_w, v2_w}')
division = input()
teams = get_teams(division)

if not os.path.isdir(division):
    os.makedirs(division)
os.chdir(division)

if not os.path.isdir('all'):
    os.makedirs('all')
os.chdir('all')

career_dir = 'career'
# print(career_dir)
if not os.path.isdir(career_dir):
    os.makedirs(career_dir)
    os.chdir(career_dir)
else:
    os.chdir(career_dir)
    for i in glob.glob('*'):
        os.remove(i)
        print('{}を削除'.format(i))

print(os.getcwd())

for team_id, team_name in teams.items():
    url = 'https://www.vleague.jp/record/team_players/{}'.format(team_id)
    print(url)
    request = req.Request(url, headers=headers)
    response = req.urlopen(request)
    parse_html = BeautifulSoup(response, 'html.parser')

    tables = parse_html.find_all('table')[0]
    tr = tables.find_all('tr')
    a = tables.find_all('a')
    player_urls = []
    for i in a:
        href = i.attrs['href']
        # print(href)
        player_url = 'https://www.vleague.jp{}'.format(href)
        # print(player_url)
        player_urls.append(player_url)
    
    number_list = []
    player_list = []
    for i in tr[1:]:
        td = i.find_all('td')
        number = td[0].text
        number_list.append(number)
        player = td[1].text.replace('\xa0', '')
        player_list.append(player)
    print(number_list, player_list)


    print(os.getcwd())

    for i in range(len(player_list)):
        html = requests.get(player_urls[i], headers=headers)
        request_2 = req.Request(player_urls[i], headers=headers)
        response_2 = req.urlopen(request_2)
        parse_html_2 = BeautifulSoup(response_2, 'html.parser')
        table_2 = parse_html_2.find_all('table')

        if len(table_2) > 0: 
            data = pd.read_html(html.text, header = [1])
            stats = pd.DataFrame(data[0])
            # print(stats)
            stats = stats.rename({"チ｜ム": "チーム", "サ｜ブ": "サーブ", "ノ｜タッチ": "ノータッチ", "エ｜ス": "エース"}, axis=1)
            stats = stats.rename(columns={'打数':'アタック打数', '得点':'アタック得点', '失点':'アタック失点', '決定率':'アタック決定率',
                                                    'セ平ット均':'アタックセット平均','打数.1':'バックアタック打数', '得点.1':'バックアタック得点',
                                                    '失点.1':'バックアタック失点', '決定率.1':'バックアタック決定率', '得点.2':'ブロック得点',
                                                    'セ平ット均.1':'ブロックセット平均', '打数.2':'サーブ打数', '得点.3':'サーブ得点', '失点.2':'サーブ失点',
                                                    '効果':'サーブ効果', '効果率':'サーブ効果率', '成功・優':'サーブレシーブ成功・優', 
                                                    '成功・良':'サーブレシーブ成功・良', '成功率':'サーブレシーブ成功率'})
            stats.insert(8, 'アタック効果率', ((stats['アタック得点'] - stats['アタック失点']) / stats['アタック打数']) * 100)
            stats.insert(13, 'バックアタック効果率', ((stats['バックアタック得点'] - stats['バックアタック失点']) / stats['バックアタック打数']) * 100)
            csv = '{0}_{1}_{2:%Y}-{2:%m}-{2:%d}.csv'.format(number_list[i], player_list[i], now)
            stats.to_csv(csv, index=False, encoding='cp932')
            print('{}を作成'.format(csv))
