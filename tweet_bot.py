import numpy as np
import pandas as pd
import os

os.chdir('/Users/sasno/Desktop/MyPandas/vleague')

df = pd.DataFrame(np.arange(12).reshape(3, 4),
                  columns=['col_0', 'col_1', 'col_2', 'col_3'],
                  index=['row_0', 'row_1', 'row_2'])

df.to_csv('tweet.csv')