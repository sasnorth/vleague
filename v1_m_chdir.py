import shutil
import os

division = 'v1_m'
team = 'JTサンダーズ広島'

os.chdir('/Users/sasno/Desktop/MyPandas/vleague/{}'.format(division))
base_path = os.getcwd()

team_list = os.listdir(base_path)
print(team_list)

for x in team_list:
    os.chdir(x)
    path = os.getcwd()
    print(path)
    files = os.listdir(path)
    files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]
    print(files_file)

    career_dir = 'career'
    # print(career_dir)
    if not os.path.isdir(career_dir):
            os.makedirs(career_dir)

    for i in files_file:
        shutil.move(i,career_dir)
    os.chdir('..')
