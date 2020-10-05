# ディレクトリ変えたことで使えない
import time
import pandas as pd
 
from bs4 import BeautifulSoup
import urllib.request as req

import requests
import os
import datetime
import re

import sys
from pathlib import Path
sys.path.append("../")
# from index.season.season_index import get_seasons

os.chdir('/Users/sasno/Desktop/MyPandas/vleague')

headers = {"User-Agent": "Mozilla/5.0"}

print('ディビジョンを選択してください:{v1_m, v2_m, v3_m, v1_w, v2_w}')
division = input()

print('年度・シーズンを選択してください:{2019-20_regular,2018-19_regular, 2017-18_regular, 2016-17_regular, 2015-14_regular}')
season = input()
# divisions = get_seasons(season)

for div_id, div_v in divisions.items():
    if division == div_v[0]:
        division_id = div_id
        pages = div_v[1]
print(division_id, division, pages)
if not os.path.isdir(division):
            os.makedirs(division)

os.chdir(division)
print(os.getcwd())

sets = ['1','2','3','4','5']

for pg in range(1,pages+1):
    url = 'https://www.vleague.jp/round/list/{0}?pg={1}'.format(division_id,pg)
    print(url)
    request = req.Request(url, headers=headers)
    response = req.urlopen(request)
    parse_html = BeautifulSoup(response, 'html.parser')
    tables = parse_html.find_all('table')

    url_list = []
    tr = tables[0].find_all('a')
    for i in range(1,len(tr),2):
        game_url = 'https://www.vleague.jp/'+ tr[i].attrs['href']
        url_list.append(game_url)

    for url in url_list:
        print(url)
        html = requests.get(url, headers=headers)
        data = pd.read_html(html.text, header=[2])

        for j in range(2):
            stats = pd.DataFrame(data[j+4])
            stats = stats.rename(columns=str)
            col = stats.columns.values
            data_item = []
            for i in col:
                l = i
                data_item.append(l)
            for i in range(1,len(data_item)-2):
                data_item[-i] = data_item[-i-3]
                # print(data_item)
            for i in range(3):
            #     print(data_item[i])
                if data_item[i] == '出場数':
                    data_item[i] = '背番号'
                elif data_item[i] == '1':
                    data_item[i] = 'リベロ'
                else:
                    data_item[i] = '名前'
            #     print(i, data_item[i])

            new_stats = stats.rename(columns={col[i]:data_item[i] for i in range(len(data_item))})
            new_stats = new_stats.rename(columns={'打数':'アタック打数', '得点':'アタック得点', '失点':'アタック失点', '決定率':'アタック決定率',
                                                    'セ平ット均':'アタックセット平均','打数.1':'バックアタック打数', '得点.1':'バックアタック得点',
                                                    '失点.1':'バックアタック失点', '決定率.1':'バックアタック決定率', '得点.2':'ブロック得点',
                                                    'セ平ット均.1':'ブロックセット平均', '打数.2':'サーブ打数', '得点.3':'サーブ得点', '失点.2':'サーブ失点',
                                                    '効果':'サーブ効果', '効果率':'サーブ効果率', '成功・優':'サーブレシーブ成功・優', 
                                                    '成功・良':'サーブレシーブ成功・良', '成功率':'サーブレシーブ成功率'})
            
            request = req.Request(url, headers=headers)
            response = req.urlopen(request)
            parse_html = BeautifulSoup(response, 'html.parser')
            table_ha = parse_html.find_all('table')[0]
            td_ha = table_ha.find_all('td', class_='team')
            # print(td_ha)
            team = td_ha[j].text
            print('team={}'.format(team))
            new_stats['アタック決定率'] = new_stats['アタック得点'] / new_stats['アタック打数']
            new_stats.insert(13, 'アタック効果率', (new_stats['アタック得点'] - new_stats['アタック失点']) / new_stats['アタック打数'])
            span = parse_html.find_all('span')
            date = span[1].text.replace('/','-')
            new_stats.insert(0, '試合日', date)
            new_stats.insert(1, 'チーム', team)
            for by_set in sets:
                new_stats[by_set] = new_stats[by_set].astype(str)
            team_dir = '{0}/{1}'.format(team,season)
            if not os.path.isdir(team_dir):
                os.makedirs(team_dir)
            new_stats.to_csv('{0}/{1}/{2}.csv'.format(team,season,date), index=False, encoding='cp932')
