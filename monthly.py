import pandas as pd
import os
import team_index

os.chdir('/Users/sasno/Desktop/MyPandas/vleague')
print('ディビジョンを選択してください:{v1_m, v2_m, v3_m, v1_w, v2_w}')
division = input()


print('年度を選択してください:{2019-20_regular,2018-19_regular, 2017-18_regular, 2016-17_regular, 2015-14_regular}')
year = input()


month_list = ['-10-', '-11-', '-12-', '-01-','-02']
set_sum = ['1','2','3','4','5']
   
team_list = os.listdir(division)
print(team_list)
os.chdir(division)

for team in team_list:
    monthly_dir = '{0}/{1}/monthly'.format(team,year)
    if not os.path.isdir(monthly_dir):
        os.makedirs(monthly_dir)
    path = '{0}\{1}'.format(team,year)
    files = os.listdir(path)
    files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]
    print(files_file)
    data_list = []
    for i in files_file:
        data = pd.read_csv('{0}\{}\{1}'.format(team, i), encoding='cp932')
        data_list.append(data[:-1])
        game_data = pd.concat(data_list, ignore_index = True)
    # print(game_data)
    player_list = game_data['名前'].unique()
    # print(len(player_list),player_list)
    for player in player_list:
        daily_stats = game_data[game_data['名前'] == player]
        # print(daily_stats)
        loc_num = 0
        header = daily_stats.columns.values
        month_stats = pd.DataFrame(columns=header)
        month_stats = month_stats.rename(columns={'試合日':'月'})
        for month in month_list:
            by_month_stats = daily_stats[daily_stats['試合日'].str.contains(month)]
            by_month_stats = by_month_stats.rename(columns={'試合日':'月'})
            # print(by_month_stats)
            if len(by_month_stats) > 0:
                month_sum = by_month_stats.sum()
                for by_set in set_sum:
                    month_sum[by_set] = by_month_stats[by_set].str.contains('■').sum()
                index = by_month_stats.index.values[0]
                print(player, index)
                ob_data = daily_stats.loc[index]
                # object型で崩れたデータを修正
                month_sum['月'] = ob_data['試合日'][5:7]
                month_sum['背番号'] = ob_data['背番号']
                month_sum['リベロ'] = ob_data['リベロ']
                month_sum['名前'] = ob_data['名前']
                if month_sum['アタック打数'] > 0:
                    month_sum['アタック決定率'] = (month_sum['アタック得点'] / month_sum['アタック打数']) * 100
                    month_sum['アタック効果率'] = ((month_sum['アタック得点'] - month_sum['アタック失点']) / month_sum['アタック打数']) * 100
                else:
                    month_sum['アタック決定率'] = None
                    month_sum['アタック効果率'] = None
                if month_sum['バックアタック打数'] > 0:
                    month_sum['バックアタック決定率'] = (month_sum['バックアタック得点'] / month_sum['バックアタック打数']) * 100
                else:
                    month_sum['バックアタック決定率'] = None
                if month_sum['出場数'] > 0:
                    month_sum['アタックセット平均'] = month_sum['アタック打数'] / month_sum['出場数']
                    month_sum['ブロックセット平均'] = month_sum['ブロック得点'] / month_sum['出場数']
                else:
                    month_sum['アタックセット平均'] = None
                    month_sum['ブロックセット平均'] = None
                if month_sum['サーブ打数'] > 0:
                    month_sum['サーブ効果率'] = ((month_sum['サーブ得点'] * 100) + (month_sum['サーブ効果'] * 25) - (month_sum['サーブ失点'] * 25)) / month_sum['サーブ打数']
                else:
                    month_sum['サーブ効果率'] = None
                if month_sum['受数'] > 0:
                    month_sum['サーブレシーブ成功率'] = ((month_sum['サーブレシーブ成功・優'] * 100) + (month_sum['サーブレシーブ成功・良'] * 50)) / month_sum['受数']
                else:
                    month_sum['サーブレシーブ成功率'] = None
                month_stats.loc[loc_num] = month_sum
                number = month_sum['背番号']
                loc_num += 1
        print(month_stats)
        month_stats.to_csv('{0}/{1}/monthly/{2}_{3}.csv'.format(team,year,number,player), index=False, encoding='cp932')
        print('{0}_{1}.csvを作成'.format(number,player))

