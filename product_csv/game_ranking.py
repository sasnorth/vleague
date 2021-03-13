import glob
import tweepy
from create_df import game_df
import time
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
import urllib.request as req

import requests
import os
import datetime
import re


def create_csv():
    daily_all = game_all[game_all['名前'] != 'チーム合計']
    daily_all = daily_all.drop(columns=[
                               '相手アタック打数', '相手アタック得点', '相手アタック失点', '相手アタック決定率', '相手ブロック得点', '相手ブロックセット平均', '相手サーブ効果率', '相手サーブレシーブ成功率'])
    daily_all['サーブ効果率'] = ((daily_all['サーブ得点'] * 100 + daily_all['サーブ効果']
                            * 25 - daily_all['サーブ失点'] * 25) / daily_all['サーブ打数']).round(1)
    daily_all['総得点'] = daily_all["アタック得点"] + \
        daily_all["ブロック得点"] + daily_all["サーブ得点"]
    year_month = daily_all['試合日'].str[0:7]
    # data = daily_all
    print(daily_all)
    daily_all.insert(1, '年月', year_month)
    daily_all.set_index('試合日')
    monthly_all = daily_all.groupby(
        ['名前', '年月', 'チーム', '背番号']).sum().reset_index()
    monthly_all['アタック決定率'] = (
        (monthly_all['アタック得点'] / monthly_all['アタック打数']) * 100).round(1)
    monthly_all['アタック効果率'] = (
        ((monthly_all['アタック得点']-monthly_all['アタック失点']) / monthly_all['アタック打数']) * 100).round(1)
    monthly_all['バックアタック決定率'] = (
        (monthly_all['バックアタック得点'] / monthly_all['バックアタック打数']) * 100).round(1)
    monthly_all['アタックセット平均'] = (
        monthly_all['アタック得点'] / monthly_all['出場数']).round(2)
    monthly_all['ブロックセット平均'] = (
        monthly_all['ブロック得点'] / monthly_all['出場数']).round(2)
    monthly_all['サーブ効果率'] = ((monthly_all['サーブ得点'] * 100 + monthly_all['サーブ効果']
                              * 25 - monthly_all['サーブ失点'] * 25) / monthly_all['サーブ打数']).round(1)
    monthly_all['サーブレシーブ成功率'] = ((monthly_all['サーブレシーブ成功・優'] * 100 +
                                  monthly_all['サーブレシーブ成功・良'] * 50) / monthly_all['受数']).round(1)
    print(monthly_all)

    yearly_all = daily_all.groupby(['名前', 'チーム', '背番号']).sum().reset_index()
    yearly_all['アタック決定率'] = (
        (yearly_all['アタック得点'] / yearly_all['アタック打数']) * 100).round(1)
    yearly_all['アタック効果率'] = (
        ((yearly_all['アタック得点']-yearly_all['アタック失点']) / yearly_all['アタック打数']) * 100).round(1)
    yearly_all['バックアタック決定率'] = (
        (yearly_all['バックアタック得点'] / yearly_all['バックアタック打数']) * 100).round(1)
    yearly_all['アタックセット平均'] = (
        yearly_all['アタック得点'] / yearly_all['出場数']).round(2)
    yearly_all['ブロックセット平均'] = (
        yearly_all['ブロック得点'] / yearly_all['出場数']).round(2)
    yearly_all['サーブ効果率'] = ((yearly_all['サーブ得点'] * 100 + yearly_all['サーブ効果']
                             * 25 - yearly_all['サーブ失点'] * 25) / yearly_all['サーブ打数']).round(1)
    yearly_all['サーブレシーブ成功率'] = ((yearly_all['サーブレシーブ成功・優'] * 100 +
                                 yearly_all['サーブレシーブ成功・良'] * 50) / yearly_all['受数']).round(1)
    print(yearly_all)

    game_all.to_csv('all/{}/game_all.csv'.format(s_round),
                    index=False, encoding='cp932')
    daily_all.to_csv('all/{}/daily_all.csv'.format(s_round),
                     index=False, encoding='cp932')
    monthly_all.to_csv('all/{}/monthly_all.csv'.format(s_round),
                       index=False, encoding='cp932')
    yearly_all.to_csv('all/{}/yearly_all.csv'.format(s_round),
                      index=False, encoding='cp932')
    print('csv作成成功')


# 2020-21の更新
os.chdir('/Users/sasno/Desktop/MyPandas/vleague')
headers = {"User-Agent": "Mozilla/5.0"}

# seasons = get_seasons(division)

s_round = "2020-21_regular"
# s_round = "2021_Vcup"
div_id = {"v1_m": ["301"], "v1_w": ["303"], "v2_m": [
    "299"], "v2_w": ["302"], "v3_m": ["300"]}
# div_id = {"v1_w": ["304", "314", "305"]}

# key
consumer_key = 'D4OAzhqT7NNeeCa9R7h0Hxzx3'
consumer_secret = 'Py8P1k5jxdPEvNOb64WUXh8b10sfDL5qr60krVLNOOLEXauZti'
access_token = '1309887734555668481-NNvdk0MCxK4WwKZCKZrOqflU9bwPfG'
access_secret = 'CmkMLM4eiOq4MLP3TE6FfUobThOElR5OAfuVSv3GRnXrJ'

# Twitterオブジェクト
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


for division, s_ids in div_id.items():
    if not os.path.isdir(division):
        os.makedirs(division)

    os.chdir(division)
    print(os.getcwd())

    sets = ['1', '2', '3', '4', '5']
    game_all = None

    # ページ数を取得
    all_list = []
    url_list = []
    for s_id in s_ids:
        url = 'https://www.vleague.jp/round/list/{}'.format(s_id)
        print(url)
        request = req.Request(url, headers=headers)
        response = req.urlopen(request)
        parse_html = BeautifulSoup(response, 'html.parser')
        hrefs = parse_html.find_all('a', href=re.compile("pg"))

        # for i in hrefs:
        #     print(i.text)
        print(len(hrefs))
        if len(hrefs) > 0:
            pages = int(hrefs[-2].text)
            print(pages)

            for pg in range(1, pages+1):
                url = 'https://www.vleague.jp/round/list/{0}?pg={1}'.format(
                    s_id, pg)
                print(url)
                request = req.Request(url, headers=headers)
                response = req.urlopen(request)
                parse_html = BeautifulSoup(response, 'html.parser')
                tables = parse_html.find_all('table')

                trs = tables[0].find_all('a', href=re.compile("/form/b"))
                for tr in trs:
                    game_url = 'https://www.vleague.jp/' + tr.attrs['href']
                    url_list.append(game_url)

        else:
            print(url)
            request = req.Request(url, headers=headers)
            response = req.urlopen(request)
            parse_html = BeautifulSoup(response, 'html.parser')
            tables = parse_html.find_all('table')

            trs = tables[0].find_all('a', href=re.compile("/form/b"))
            for tr in trs:
                game_url = 'https://www.vleague.jp/' + tr.attrs['href']
                url_list.append(game_url)

    print(url_list)

    for url in url_list:
        # print(url)
        try:
            html = requests.get(url, headers=headers)
            check = html.text
            if '試合データがありません' not in check and '試合データの集計中です。しばらくお待ちください。' not in check:
                # try:
                data = pd.read_html(check, header=[2])

                for j in range(2):
                    stats = pd.DataFrame(data[j+4])
                    o_stats = pd.DataFrame(data[-(j+1)])
                    stats = stats.rename(columns=str)
                    o_stats = o_stats.rename(columns=str)
                    col = stats.columns.values
                    data_item = []
                    for i in col:
                        l = i
                        data_item.append(l)
                    for i in range(1, len(data_item)-2):
                        data_item[-i] = data_item[-i-3]
                #     print(data_item)
                    for i in range(3):
                        #     print(data_item[i])
                        if data_item[i] == '出場数':
                            data_item[i] = '背番号'
                        elif data_item[i] == '1':
                            data_item[i] = 'リベロ'
                        else:
                            data_item[i] = '名前'
                        # print(i, data_item[i])

                    new_stats = stats.rename(
                        columns={col[i]: data_item[i] for i in range(len(data_item))})
                    stats_columns = {
                        '打数': 'アタック打数', '得点': 'アタック得点', '失点': 'アタック失点', '決定率': 'アタック決定率',
                        'セ平ット均': 'アタックセット平均', '打数.1': 'バックアタック打数', '得点.1': 'バックアタック得点',
                        '失点.1': 'バックアタック失点', '決定率.1': 'バックアタック決定率', '得点.2': 'ブロック得点',
                        'セ平ット均.1': 'ブロックセット平均', '打数.2': 'サーブ打数', '得点.3': 'サーブ得点', '失点.2': 'サーブ失点',
                        '効果': 'サーブ効果', '効果率': 'サーブ効果率', '成功・優': 'サーブレシーブ成功・優',
                        '成功・良': 'サーブレシーブ成功・良', '成功率': 'サーブレシーブ成功率'
                    }
                    new_o_stats = o_stats.rename(
                        columns={col[i]: data_item[i] for i in range(len(data_item))})
                    new_stats = new_stats.rename(columns=stats_columns)
                    new_o_stats = new_o_stats.rename(columns=stats_columns)
                    new_o_stats = new_o_stats.rename(columns={'アタック打数': '相手アタック打数', 'アタック得点': '相手アタック得点', 'アタック失点': '相手アタック失点',
                                                              'アタック決定率': '相手アタック決定率', 'ブロック得点': '相手ブロック得点', 'ブロックセット平均': '相手ブロックセット平均',
                                                              'サーブ効果率': '相手サーブ効果率', 'サーブレシーブ成功率': '相手サーブレシーブ成功率'})
                    new_o_stats_p = new_o_stats.iloc[-1][['背番号', '相手アタック打数', '相手アタック得点', '相手アタック失点', '相手アタック決定率', '相手ブロック得点', '相手ブロックセット平均',
                                                          '相手サーブ効果率', '相手サーブレシーブ成功率']]
                    new_o_stats_p = pd.DataFrame(new_o_stats_p).T
                #     new_o_stats_p

                    request = req.Request(url, headers=headers)
                    response = req.urlopen(request)
                    parse_html = BeautifulSoup(response, 'html.parser')
                    table_ha = parse_html.find_all('table')[0]
                    td_ha = table_ha.find_all('td', class_='team')
                    # print(td_ha)
                    team = td_ha[j].text
                    # print('team={}'.format(team))
                    new_stats['アタック決定率'] = (new_stats['アタック得点'] *
                                            100 / new_stats['アタック打数']).round(1)
                    new_stats.insert(13, 'アタック効果率',
                                     ((new_stats['アタック得点'] - new_stats['アタック失点']) * 100 / new_stats['アタック打数']).round(1))
                    span = parse_html.find_all('span')
                    date = span[1].text.replace('/', '-')
                    new_stats.insert(0, '試合日', date)
                    new_stats.insert(1, 'チーム', team)
                    new_stats['名前'] = new_stats['名前'].str.replace('\u3000', '')
                    for by_set in sets:
                        new_stats[by_set] = new_stats[by_set].astype(str)
                    team_dir = '{0}/{1}'.format(team, s_round)

                    stats_m = pd.merge(new_stats, new_o_stats_p,
                                       on='背番号', how='outer')
                #     stats_m
                    if not os.path.isdir(team_dir):
                        os.makedirs(team_dir)
                    stats_m.to_csv('{0}/{1}/{2}.csv'.format(team,
                                                            s_round, date), index=False, encoding='cp932')
                    all_list.append(stats_m)
        except:
            pass
    #     print(all_list)
    game_all = pd.concat(all_list, ignore_index=True)

    all_dir = 'all/{}'.format(s_round)
    if not os.path.isdir(all_dir):
        os.makedirs(all_dir)

    print(os.getcwd())
    try:
        create_csv()
    except:
        pass

    if 'm' in division:
        division_j = 'V' + division[1] + '男子'
    else:
        division_j = 'V' + division[1] + '女子'

    daily_all = pd.read_csv(
        'all/{}/daily_all.csv'.format(s_round), encoding='cp932')
    # daily_all
    day = '2021-03-13'
    today_data = daily_all[daily_all['試合日'] == day]

    if len(today_data) > 0:
        # today_data.head()
        stats_list = ['total', 'at_attack', 'attack_k',
                      'b_attack_k', 'block', 'surve_k', 'surve_eff', 'cut']
        # stats = np.random.choice(stats_list)
        for stats in stats_list:
            print(stats)
            if stats == 'total':
                reg_judge = today_data['出場数'] >= 1
                column = '総得点'
                pattern = ['出場数1セット', 2]
            elif stats == 'at_attack':
                reg_judge = today_data['出場数'] >= 1
                column = 'アタック打数'
                pattern = ['出場数1セット', 0]
            elif stats == 'attack_k':
                reg_judge = today_data['アタック打数'] >= 10
                column = 'アタック決定率'
                pattern = ['打数10本', 1]
            elif stats == 'b_attack_k':
                reg_judge = today_data['バックアタック打数'] >= 5
                column = 'バックアタック決定率'
                pattern = ['打数5本', 1]
            elif stats == 'block':
                reg_judge = today_data['出場数'] >= 2
                column = 'ブロックセット平均'
                pattern = ['出場数2セット', 0]
            elif stats == 'surve_k':
                reg_judge = today_data['サーブ打数'] >= 5
                column = 'サーブ得点'
                pattern = ['サーブ打数5本', 2]
            elif stats == 'surve_eff':
                reg_judge = today_data['サーブ打数'] >= 5
                column = 'サーブ効果率'
                pattern = ['サーブ打数5本', 1]
            else:
                reg_judge = today_data['受数'] >= 5
                column = 'サーブレシーブ成功率'
                pattern = ['受数5本', 1]
            print(column)

            for i in range(3):
                stats_df = today_data[reg_judge][[
                    '名前', 'チーム', '背番号', '出場数', column]]
                stats_df = stats_df.sort_values(column, ascending=False).head()
                print(stats_df)
                if len(stats_df) >= 3:
                    break
            # try:
            # stats_df = stats_df.to_dict()
            # print(stats_df)

            p = re.compile('[\u0000-\u007F]+')
            messages = '本日({})の成績\n'.format(day)
            messages += 'シーズン: {}\n'.format(s_round)
            messages += '【{0}】ランキング({1}以上)\n'.format(column, pattern[0])
            messages += 'ディビジョン: #{}\n'.format(division_j)
            print(len(stats_df))
            for i in range(len(stats_df)):
                if pattern[1] == 1:
                    message = '{0}位 #{1} ({2}, {3}%)\n'.format(
                        i+1, stats_df['名前'].iloc[i], stats_df['チーム'].iloc[i], stats_df[column].iloc[i])
                elif pattern[1] == 2:
                    message = '{0}位 #{1} ({2}, {3}点)\n'.format(
                        i+1, stats_df['名前'].iloc[i], stats_df['チーム'].iloc[i], stats_df[column].iloc[i])
                else:
                    message = '{0}位 #{1} ({2}, {3}本)\n'.format(
                        i+1, stats_df['名前'].iloc[i], stats_df['チーム'].iloc[i], stats_df[column].iloc[i])
                m_len = messages + message
                m_len = messages + message
                e_len = len(''.join(p.findall(m_len)))
                tweet_len = len(m_len) - (e_len/2)
                # print(tweet_len)
                if tweet_len <= 140:
                    messages += message
                else:
                    break
            print(messages)
            # api.update_status(messages)
            # except:
            #     pass

    yearly_all = pd.read_csv(
        'all/{}/yearly_all.csv'.format(s_round), encoding='cp932')
    if division == 'v1_m':
        n = 25
    elif division == 'v2_m' or division == 'v1_w':
        n = 20
    elif division == 'v2_w':
        n = 10
    else:
        n = 5

    if len(yearly_all) > 0:
        stats_list = ['total', 'at_attack', 'attack_k',
                      'b_attack_k', 'block', 'surve_k', 'surve_eff', 'cut']
        # stats = np.random.choice(stats_list)
        for stats in stats_list:
            print(stats)
            if stats == 'total':
                reg_judge = yearly_all['出場数'] >= n
                column = '総得点'
                pattern = ['出場数{}セット'.format(n), 2]
            elif stats == 'at_attack':
                reg_judge = yearly_all['出場数'] >= n
                column = 'アタック打数'
                pattern = ['出場数{}セット'.format(n), 0]
            elif stats == 'attack_k':
                reg_judge = yearly_all['アタック打数'] >= n*10
                column = 'アタック決定率'
                pattern = ['打数{}本'.format(n*10), 1]
            elif stats == 'b_attack_k':
                reg_judge = yearly_all['バックアタック打数'] >= n*4
                column = 'バックアタック決定率'
                pattern = ['打数{}本'.format(n*4), 1]
            elif stats == 'block':
                reg_judge = yearly_all['出場数'] >= n
                column = 'ブロックセット平均'
                pattern = ['出場数{}セット'.format(n), 0]
            elif stats == 'surve_k':
                reg_judge = yearly_all['サーブ打数'] >= n*5
                column = 'サーブ得点'
                pattern = ['サーブ打数{}本'.format(n*5), 2]
            elif stats == 'surve_eff':
                reg_judge = yearly_all['サーブ打数'] >= n*5
                column = 'サーブ効果率'
                pattern = ['サーブ打数{}本'.format(n*5), 1]
            else:
                reg_judge = yearly_all['受数'] >= n*10
                column = 'サーブレシーブ成功率'
                pattern = ['受数{}本'.format(n*10), 1]
            print(column)

            for i in range(3):
                stats_df = yearly_all[reg_judge][[
                    '名前', 'チーム', '背番号', '出場数', column]]
                stats_df = stats_df.sort_values(column, ascending=False).head()
                print(stats_df)
                if len(stats_df) >= 3:
                    break
            # try:
            # stats_df = stats_df.to_dict()
            print(stats_df)
            p = re.compile('[\u0000-\u007F]+')
            messages = '今シーズン({})通算成績\n'.format(s_round)
            messages += '【{0}】ランキング({1}以上)\n'.format(column, pattern[0])
            messages += 'ディビジョン: #{}\n'.format(division_j)
            print(len(stats_df))
            for i in range(len(stats_df)):
                if pattern[1] == 1:
                    message = '{0}位 #{1} ({2}, {3}%)\n'.format(
                        i+1, stats_df['名前'].iloc[i], stats_df['チーム'].iloc[i], stats_df[column].iloc[i])
                elif pattern[1] == 2:
                    message = '{0}位 #{1} ({2}, {3}点)\n'.format(
                        i+1, stats_df['名前'].iloc[i], stats_df['チーム'].iloc[i], stats_df[column].iloc[i])
                else:
                    message = '{0}位 #{1} ({2}, {3}本)\n'.format(
                        i+1, stats_df['名前'].iloc[i], stats_df['チーム'].iloc[i], stats_df[column].iloc[i])
                m_len = messages + message
                m_len = messages + message
                e_len = len(''.join(p.findall(m_len)))
                tweet_len = len(m_len) - (e_len/2)
                # print(tweet_len)
                if tweet_len <= 140:
                    messages += message
                else:
                    break
            print(messages)
            # api.update_status(messages)
            # except:
            #     pass
    os.chdir('../')
