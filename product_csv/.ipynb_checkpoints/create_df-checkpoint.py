import time
import numpy as np
import pandas as pd
 
from bs4 import BeautifulSoup
import urllib.request as req
 
import requests
import os
import datetime
import re

headers = {"User-Agent": "Mozilla/5.0"}

sets = ['1','2','3','4','5']

def game_df(url, s_round, all_list):
    headers = {"User-Agent": "Mozilla/5.0"}
    request = req.Request(url, headers=headers)
    response = req.urlopen(request)
    parse_html = BeautifulSoup(response, 'html.parser')
    hrefs = parse_html.find_all('a', href=re.compile("pg"))
 
    # for i in hrefs:
    #     print(i.text)
    if len(hrefs) > 0:
        pages = int(hrefs[-2].text)
        print(pages)

        for pg in range(1,pages+1):
            url_pg = 'https://www.vleague.jp/round/list/{0}?pg={1}'.format(s_id,pg)
            print(url_pg)
            request = req.Request(url_pg, headers=headers)
            response = req.urlopen(request)
            parse_html = BeautifulSoup(response, 'html.parser')
            tables = parse_html.find_all('table')

            url_list = []
            trs = tables[0].find_all('a', href=re.compile("/form/b"))
            for tr in trs:
                game_url = 'https://www.vleague.jp/'+ tr.attrs['href']
                url_list.append(game_url)
            print(url_list)

            for url_game in url_list:
                # print(url)
                html = requests.get(url_game, headers=headers)
                check = html.text
                if '試合データがありません' not in check and '試合データの集計中です。しばらくお待ちください。' not in check:
                    data = pd.read_html(check, header=[2])

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
                        new_stats = new_stats.rename(columns={
                            '打数':'アタック打数', '得点':'アタック得点', '失点':'アタック失点', '決定率':'アタック決定率',
                            'セ平ット均':'アタックセット平均','打数.1':'バックアタック打数', '得点.1':'バックアタック得点',
                            '失点.1':'バックアタック失点', '決定率.1':'バックアタック決定率', '得点.2':'ブロック得点',
                            'セ平ット均.1':'ブロックセット平均', '打数.2':'サーブ打数', '得点.3':'サーブ得点', '失点.2':'サーブ失点',
                            '効果':'サーブ効果', '効果率':'サーブ効果率', '成功・優':'サーブレシーブ成功・優', 
                            '成功・良':'サーブレシーブ成功・良', '成功率':'サーブレシーブ成功率'
                            })

                        request = req.Request(url_game, headers=headers)
                        response = req.urlopen(request)
                        parse_html = BeautifulSoup(response, 'html.parser')
                        table_ha = parse_html.find_all('table')[0]
                        td_ha = table_ha.find_all('td', class_='team')
                        td_set = table_ha.find_all('td', class_='b')
                        # print(td_ha)
                        team = td_ha[j].text
                        o_team = td_ha[-(j+1)].text
                        print('team={}, o_team={}'.format(team, o_team))
                        get_set = int(td_set[0].text)
                        lost_set = int(td_set[-2].text)
                        if j==1:
                            get_set, lost_set = lost_set, get_set
                        print('get_set={}, lost_set={}'.format(get_set, lost_set))
                        if get_set == 3:
                            win_lose = 1
                        else:
                            win_lose = 0
                        print('win_lose={}'.format(win_lose))

                        new_stats['アタック決定率'] = ((new_stats['アタック得点'] / new_stats['アタック打数']) * 100).round(1)
                        new_stats.insert(13, 'アタック効果率',
                            (((new_stats['アタック得点'] - new_stats['アタック失点']) / new_stats['アタック打数']) * 100).round(1))
                        new_stats['総得点'] = new_stats['アタック得点'] + new_stats['ブロック得点'] + new_stats['サーブ得点']
                        span = parse_html.find_all('span')
                        date = span[1].text.replace('/','-')
                        new_stats.insert(0, '試合日', date)
                        new_stats.insert(1, 'チーム', team)
                        new_stats.insert(2, '相手チーム', o_team)
                        new_stats.insert(3, '得セット', get_set)
                        new_stats.insert(4, '失セット', lost_set)
                        new_stats.insert(5, '勝敗', win_lose)
                        new_stats['名前'] = new_stats['名前'].str.replace('\u3000','')
                        for by_set in sets:
                            new_stats[by_set] = new_stats[by_set].astype(str)
                        # 必要に応じてteamディレクトリを作成
                        team_dir = '{0}/{1}'.format(team,s_round)
                        if not os.path.isdir(team_dir):
                            os.makedirs(team_dir)
                        new_stats.to_csv('{0}/{1}/{2}.csv'.format(team,s_round,date), index=False, encoding='cp932')
                        print(new_stats)
                        all_list.append(new_stats)