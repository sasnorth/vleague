# vleague

VリーグのデータをCSV化するためのプログラムです。
最近は、twitterbotを動かすためのプログラムも作成しています。

※途中過程でアップロードすることもあるため、コードが度々変更することがあります。

## csvの説明
カンファレンス(v1_mなど)のフォルダにあるcsvについて説明します。
ディレクトリ構成は主に、vleague/カンファレンス/all/*.csvとなっております。
### game_all.csv
後に説明する、B帳簿から読み取れるデータをスクレイピングして、そのままcsvにしたものです。
※後に被アタック決定率等の、相手の指標も追加しました。

### daily_all.csv
game_all.csvから、選手別の成績を抽出したものです。

### monthly_all.csv
daily_all.csvから、選手別の成績を月別でまとめたものです。

### yearly_all.csv
daily_all.csvから、選手別の成績を年別でまとめたものです。
twitterのbotには主にこれを用いています。
