# R 3.2.4

library(data.table)
library(reshape2)
library(ggplot2)

dt_results_round_two <- fread("./data/output/results_round_two.csv")

dt_results_round_two <- dt_results_round_two[ distrito !="TODOS" & porc_valid >0]

dt_results_round_two <- dt_results_round_two[, perc_not_val:= 100  - sum(porc_emit) , by = ubigeo ]





dt_results_round_one <- fread("./data/output/results_round_one.csv")

dt_results_round_one <- dt_results_round_one[ distrito !="TODOS" & perc_valid >0]

dt_results_round_one <- dt_results_round_one[, perc_not_val:= 100  - sum(perc_emit) , by = ubigeo ]
dt_results_round_one[ , perc_valid:= as.numeric(perc_valid)]

dt_one <- dt_results_round_one[ ,.(ppk= perc_valid[  party =="PERUANOS POR EL KAMBIO "] ,
                                   fa= perc_valid[  party =="EL FRENTE AMPLIO POR JUSTICIA, VIDA Y LIBERTAD "]), keyby = ubigeo]

dt_not_val <- unique(dt_results_round_two[ , .(perc_not_val)])

ggplot(dt_results_round_two, aes(x= porc_valid, color = party))+ geom_density()

ggplot(dt_not_val, aes(x= perc_not_val))+ geom_density()

dt_results_round_two[ votes == 0]

#problema potencial
#dt_results_round_two[ , .(.N) , keyby = party]
#party    N
#1:         FUERZA POPULAR  2063
#2: PERUANOS POR EL KAMBIO  2067


dt_ppk <- dt_results_round_two[ party =="PERUANOS POR EL KAMBIO "]
dt_ppk <- merge(dt_ppk, dt_one , by = "ubigeo", all.x=T)

cor( dt_ppk[ , .(porc_valid,perc_not_val,ppk,fa)],use = "pairwise.complete.obs")

ggplot( dt_ppk, aes( x= fa, y= porc_valid))+geom_point()

ggplot( dt_ppk, aes( x= ppk, y= porc_valid))+geom_point() + coord_equal()


