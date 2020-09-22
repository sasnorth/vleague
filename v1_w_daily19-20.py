import pandas as pd
import os

os.chdir('/Users/sasno/Desktop/MyPandas/vleague')

division = 'v1_w'

team_list = os.listdir(division)
print(team_list)

for x in team_list:
    print('チーム:{}'.format(x))
    # ディレクトリ：dailyを作成
    daily_dir = r'{0}\{1}\game_2019-20\daily'.format(division,x)
    if not os.path.isdir(daily_dir):
        os.makedirs(daily_dir)
        
    # ファイル名だけを取得
    path = r'{0}\{1}\game_2019-20'.format(division,x)
    files = os.listdir(path)
    files_list = [f for f in files if os.path.isfile(os.path.join(path, f))]
    # print(files_list)

    # 新設チームにデータが無いためスキップする
    if len(files_list) > 0:
        data_list = []
        for i in files_list:
            data = pd.read_csv(r'{0}\{1}\game_2019-20\{2}'.format(division,x,i), encoding='cp932')
            # 最後の1行の値：'チーム合計'を含まないようにしている
            data_list.append(data[:-1])
        game_data = pd.concat(data_list, ignore_index = True)
        u = game_data['名前'].unique()
        # print(len(u),u)
        for i in u:
            player_list = game_data[game_data['名前'] == i]
            player_list.to_csv('{0}/game_2019-20/daily/{1}_{2}_dailystats.csv'.format(division,x,i), index=False, encoding='cp932')
            print('{}_dailystats.csvを作成'.format(i))