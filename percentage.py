def pctg(df, pctg, kill, total):
    if df[total] > 0:
        df[pctg] = ((df[kill] / df[total]) * 100).round(1)
    else:
        df[pctg] = None

def eff(df, eff, kill, miss, total):
    if df[total] > 0:
        df[eff] = (((df[kill] - df[miss]) / df[total]) * 100).round(1)
    else:
        df[eff] = None

def per_set(df, per_set, kill, game):
    if df[game] > 0:
        df[per_set] = (df[kill] / df[game]).round(1)
    else:
        df[per_set] = None

def serve_eff(df, serve_eff, kill, eff, miss, total):
    if df[total] > 0:
        df[serve_eff] = ((df[kill] * 100 + df[eff] * 25 - df[miss] * 25) / df[total]).round(1)
    else:
        df[serve_eff] = None

def cut_pctg(df, cut_pctg, s_great, s_good, total):
    if df[total] > 0:
        df[cut_pctg] = ((df[s_great] * 100 + df[s_good] * 50) / df[total]).round(1)
    else:
        df[cut_pctg] = None