def get_seasons(season):
    # 19-20シーズン
    if season == '2019-20_regular':
        return {
            # id: [division, ページ数]
            "283": ["v1_m", 7],
            "288": ["v2_m", 6],
            "287": ["v3_m", 2],
            "277": ["v1_w", 7],
            "281": ["v2_w", 5]
        }
    elif season == '2018-19_regular':
        return {
            "":[]
        }