import pandas as pd

df_results_round_two = pd.DataFrame()
df_ambito = df_results_round_two[ df_results_round_two ['ambito'] == 'TODOS' ]

df_dist = df_results_round_two[ df_results_round_two ['distrito'] != 'TODOS' ]


df_dist[ ['party', 'votes']].groupby('party').sum()


def checkSubLevelMatch(df_upper, df_lower, l_lower_agg_var):



    return( )