import pandas as pd
import os

os.chdir('/Users/sasno/Desktop/MyPandas/vleague')

print('ディビジョンを選択してください:{v1_m, v2_m, v3_m, v1_w, v2_w}')
division = input()

print('年度・シーズンを選択してください:{2019-20_regular,2018-19_regular, 2017-18_regular, 2016-17_regular, 2015-14_regular}')
season = input()

team_list = os.listdir(division)
print(team_list)
os.chdir(division)

for team in team_list:
    print('チーム:{}'.format(team))
    # ディレクトリ：dailyを作成
    daily_dir = r'{0}\{1}\daily'.format(team,season)
    if not os.path.isdir(daily_dir):
        os.makedirs(daily_dir)
        
    # ファイル名だけを取得
    path = r'{0}\{1}'.format(team,season)
    files = os.listdir(path)
    files_list = [f for f in files if os.path.isfile(os.path.join(path, f))]
    # print(files_lists)
    data_list = []
    if len(files_list) > 0:
        for i in files_list:
            data = pd.read_csv('{0}/{1}/{2}'.format(team,season,i), encoding='cp932')
            # 最後の1行の値：'チーム合計'を含まないようにしている
            data_list.append(data[:-1])
        game_data = pd.concat(data_list, ignore_index=True)
        print(game_data)
        player_list = game_data['名前'].unique()
        number_list = game_data['背番号'].unique()
        # print(len(player_list),player_list)
        for i in range(len(player_list)):
            daily_stats = game_data[game_data['名前'] == player_list[i]]
            daily_stats.to_csv('{0}/{1}/daily/{2}_{3}_dailystats.csv'.format(team,season,number_list[i],player_list[i]), index=False, encoding='cp932')
            print('{0}_{1}_dailystats.csvを作成'.format(number_list[i],player_list[i]))