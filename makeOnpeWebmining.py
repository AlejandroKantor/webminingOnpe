#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python 3.5
# selenium connects to firefox 47.0.1

#----------------------------------------------------------------------------
#     ____                           __     __  ___          __      __
#    /  _/___ ___  ____  ____  _____/ /_   /  |/  /___  ____/ /_  __/ /__  _____
#    / // __ `__ \/ __ \/ __ \/ ___/ __/  / /|_/ / __ \/ __  / / / / / _ \/ ___/
#  _/ // / / / / / /_/ / /_/ / /  / /_   / /  / / /_/ / /_/ / /_/ / /  __(__  )
# /___/_/ /_/ /_/ .___/\____/_/   \__/  /_/  /_/\____/\__,_/\__,_/_/\___/____/
#              /_/
#----------------------------------------------------------------------------


import pickle # for saving objects

# import functions from user script
from scripts.functions import *


#----------------------------------------------------------------------------
#     _______           __     ____                        __
#    / ____(_)_________/ /_   / __ \____  __  ______  ____/ /
#   / /_  / / ___/ ___/ __/  / /_/ / __ \/ / / / __ \/ __  /
#  / __/ / / /  (__  ) /_   / _, _/ /_/ / /_/ / / / / /_/ /
# /_/   /_/_/  /____/\__/  /_/ |_|\____/\__,_/_/ /_/\__,_/
#----------------------------------------------------------------------------

# set url of second round results
s_url = 'https://www.web.onpe.gob.pe/modElecciones/elecciones/elecciones2016/PRPCP2016/Resultados-Ubigeo-Presidencial.html#posicion'

d_results_round_one = makeOnpeWebmining(s_url)

df_results_round_one = d_results_round_one[ 'df_results']
df_vote_type_round_one = d_results_round_one[ 'df_vote_type']

df_results_round_one.to_csv( './data/output/results_round_one.csv', index=False)
df_vote_type_round_one.to_csv( './data/output/vote_type_round_one.csv', index=False)

pickle.dump(d_results_round_one, open( "./data/output/d_results_round_one.p", "wb" ))


#----------------------------------------------------------------------------
#    _____                           __   ____                        __
#   / ___/___  _________  ____  ____/ /  / __ \____  __  ______  ____/ /
#   \__ \/ _ \/ ___/ __ \/ __ \/ __  /  / /_/ / __ \/ / / / __ \/ __  /
#  ___/ /  __/ /__/ /_/ / / / / /_/ /  / _, _/ /_/ / /_/ / / / / /_/ /
# /____/\___/\___/\____/_/ /_/\__,_/  /_/ |_|\____/\__,_/_/ /_/\__,_/
# ----------------------------------------------------------------------------

# set url of first round results
s_url = 'https://www.web.onpe.gob.pe/modElecciones/elecciones/elecciones2016/PRP2V2016/Resultados-Ubigeo-Presidencial.html#posicion'

d_results_round_two = makeOnpeWebmining(s_url)

# save results as csv and dictionary object

df_results_round_two = d_results_round_two[ 'df_results']
df_vote_type_round_two = d_results_round_two[ 'df_vote_type']

df_results_round_two.to_csv( './data/output/results_round_two.csv', index=False)
df_vote_type_round_two.to_csv( './data/output/vote_type_round_two.csv', index=False)

pickle.dump(d_results_round_two, open( "./data/output/d_results_round_two.p", "wb" ))