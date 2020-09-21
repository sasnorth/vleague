import pandas as pd
import os

os.chdir('/Users/sasno/Desktop/MyPandas/vleague')
division = 'v1_m'



team_list = os.listdir(division)
print(team_list)

for x in team_list:
    print('チーム:{}'.format(x))
    # ディレクトリ：dailyを作成
    daily_dir = '{0}\{1}\game_2019-20\daily'.format(division,x)
    if not os.path.isdir(daily_dir):
        os.makedirs(daily_dir)
        
    # ファイル名だけを取得
    path = '{0}\{1}\game_2019-20'.format(division,x)
    files = os.listdir(path)
    files_list = [f for f in files if os.path.isfile(os.path.join(path, f))]
    # print(files_file)
    data_list = []
    for i in files_list:
        data = pd.read_csv(r'C:\Users\sasno\Desktop\MyPandas\vleague\{0}\{1}\game_2019-20\{2}'.format(division,x,i), encoding='cp932')
        # 最後の1行の値：'チーム合計'を含まないようにしている
        data_list.append(data[:-1])
    game_data = pd.concat(data_list, ignore_index = True)
    player_list = game_data['名前'].unique()
    number_list = game_data['背番号'].unique()
    # print(len(player_list),player_list)
    for i in range(len(player_list)):
        daily_stats = game_data[game_data['名前'] == player_list[i]]
        daily_stats.to_csv('/Users/sasno/Desktop/MyPandas/vleague/{0}/{1}/game_2019-20/daily/{2}_{3}_dailystats.csv'.format(division,x,number_list[i],player_list[i]), index=False, encoding='cp932')
        print('{}_dailystats.csvを作成'.format(i))