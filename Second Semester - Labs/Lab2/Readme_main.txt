MAIN

Il codice gira in circa 3 ore (credo si possa far girare più volte in contemporanea perché una singola run usa solo una bassa percentuale del processore, quindi dovrebbero comunque finire in 3 ore)

Obiettivo: ottenere grafici del service time per diverse situazioni (ogni risultato deve avere confidence intervals)

SIMULAZIONI:
1) con diversa LINK_CAPACITY dei server (per ora nel codice ci sono 10Gbps, 10Mbps e 10kbps, se ne possono aggiungere altre)
2) con diverso numero dei server (il file Amazon_servers_stations contiene 52 server, Amazon_servers_stations2 ne contiene 16, se ne potrebbe creare ancora uno con 3 server (uno in Europa, uno in Asia, uno in America))
3) con diversa MAX_REQ (ha senso?)

1)
-usare Amazon_servers_stations2 e MAX_REQ=10
-per ogni valore di LINK_CAPACITY ripetere simulazione almeno 5 volte (magari con diverso random_seed o mettendo il random seed che cambia con il tempo), salvare i risultati del service time su excel, calcolare valor medio e deviazione standard
-creare grafico con i valori di LINK_CAPACITY sull\'92asse x e risultati service time sulle y (i risultati devono essere accompagnati dal confidence interval, cioè si deve vedere valor medio +/- deviazione standard, credo)

2)
-usare LINK_CAPACITY=10Mbps e MAX_REQ=10
-per cambiare file dei server bisogna modificare il nome del file in Server.py e in map.py (mi pare compaia una volta sola in entrambi)\
-per ogni valore  di numero di server ripetere simulazione almeno 5 volte (magari con diverso random_seed), salvare i risultati del service time su excel, calcolare valor medio e deviazione standard
-creare grafico con il numero di servers sull'asse x e risultati service time sulle y (i risultati devono essere accompagnati dal confidence interval, cioè si deve vedere valor medio +/- deviazione standard, credo)

3) (se vogliamo fare anche questa)
-usare LINK_CAPACITY=10Mbps e Amazon_servers_stations2
-per ogni valore  di MAX_REQ ripetere simulazione almeno 5 volte (magari con diverso random_seed), salvare i risultati del service time su excel, calcolare valor medio e deviazione standard
-creare grafico con i valori di MAX_REQ sull'asse x e risultati service time sulle y (i risultati devono essere accompagnati dal confidence interval, cioè si deve vedere valor medio +/- deviazione standard, credo)


MAIN_ex2 

Dovrebbe di nuovo girare in 3 ore (non ho ancora provato)

Obiettivo: vedi sopra

Per le simulazioni valgono le stesse considerazioni del main

SIMULAZIONI:
1) con diversa LINK_CAPACITY
2) diverso numero iniziale di server on
3) se riesco faccio anche un main_ex2_v2 con una diversa strategia di accensione/spegnimento
