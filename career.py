import time
import pandas as pd
 

from bs4 import BeautifulSoup
import urllib.request as req

import requests
import os
import datetime
import re
import glob


now = datetime.datetime.now()
w_team_num = 12

os.chdir('/Users/sasno/Desktop/MyPandas/vleague')

headers = {"User-Agent": "Mozilla/5.0"}

print('ディビジョンを選択してください:{v1_m, v2_m, v3_m, v1_w, v2_w}')
division = input()

if division == 'v1_m':
    teams = {
        "268":"ジェイテクトSTINGS",
        "256":"パナソニックパンサーズ",
        "252":"サントリーサンバーズ",
        "255":"JTサンダーズ",
        "251":"堺ブレイザーズ",
        "257":"東レアローズ",
        "258":"ウルフドッグス名古屋",
        "253":"FC東京",
        "259":"大分三好ヴァイセアドラー",
        "461":"VC長野トライデンツ"
    }

if division == 'v2_m':
    teams = {
        "272":"富士通カワサキレッドスピリッツ",
        "479":"ヴォレアス北海道",
        "455":"埼玉アザレア",
        "274":"トヨタ自動車サンホークス",
        "270":"大同特殊鋼レッドスター",
        "480":"ヴィアティン三重",
        "271":"つくばユナイテッドSunGAIA",
        "269":"警視庁フォートファイターズ",
        "296":"きんでんトリニティーブリッツ",
        "267":"東京ヴェルディ",
        "290":"兵庫デルフィーノ",
        "474":"長野GaRons",
        "483":"サフィルヴァ北海道"
    }

if division == 'v3_m':
    teams = {
        "462":"奈良ドリーマーズ",
        "273":"近畿クラブスフィーダ",
        "297":"トヨタモビリティ東京スパークル",
        "460":"千葉ZELVA",
        "491":"アイシンティルマーレ",
        "490":"クボタスピアーズ"
    }

if division == 'v1_w':
    teams = {
        "285":"JTマーヴェラス",
        "263":"岡山シーガルズ",
        "281":"埼玉上尾メディックス",
        "265":"デンソーエアリービーズ",
        "266":"トヨタ車体クインシーズ",
        "283":"東レアローズ",
        "261":"久光スプリングス",
        "284":"NECレッドロケッツ",
        "264":"日立リヴァーレ",
        "277":"KUROBEアクアフェアリーズ",
        "275":"PFUブルーキャッツ",
        "481":"ヴィクトリーナ姫路"
    }

if division == 'v2_w':
    teams = {
        "458":"群馬銀行グリーンウイングス",
        "299":"GSS東京サンビームズ",
        "447":"JAぎふリオレーナ",
        "484":"ルートインホテルズブリリアントアリーズ",
        "457":"プレステージ・インターナショナルアランマーレ",
        "279":"大野石油広島オイラーズ",
        "280":"千葉エンゼルクロス",
        "459":"ブレス浜松",
        "298":"フォレストリーヴズ熊本"
    }

if not os.path.isdir(division):
    os.makedirs(division)
os.chdir(division)
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

    if not os.path.isdir(team_name):
        os.makedirs(team_name)
    os.chdir(team_name)
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

    for i in range(len(player_list)):
        html = requests.get(player_urls[i], headers=headers)
        request_2 = req.Request(player_urls[i], headers=headers)
        response_2 = req.urlopen(request_2)
        parse_html_2 = BeautifulSoup(response_2, 'html.parser')
        table_2 = parse_html_2.find_all('table')

        if len(table_2) > 0: 
            data = pd.read_html(html.text, header = [0, 1])
            stats = pd.DataFrame(data[0])
            stats = stats.rename({"チ｜ム":"チーム", "サ｜ブ":"サーブ", "ノ｜タッチ":"ノータッチ", "エ｜ス":"エース"}, axis=1)
            csv = '{0}_{1}_{2:%Y}-{2:%m}-{2:%d}.csv'.format(number_list[i], player_list[i], now)
            stats.to_csv(csv, index=False, encoding='cp932')
            print('{}を作成', csv)
    os.chdir('../..')
    print(os.getcwd)

