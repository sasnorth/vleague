import numpy as np
import pandas as pd

import os
import glob
import re

os.chdir('/Users/sasno/Desktop/MyPandas/vleague')
division = 'v1_w'
os.chdir(division)
print(os.getcwd())
s_round = '2020-21_regular'
h_team = '日立*'
day = '*'
livescore_lists = glob.glob(
    'all/{}/{}-livescore-{}vs*.csv'.format(s_round, day, h_team))
print(len(livescore_lists))
# print(livescore_lists)
for i in livescore_lists:
    print(i[20:30])
#     print(i)
# home_game_log = pd.read_csv(livescore_lists[1])
# home_game_log.tail()
