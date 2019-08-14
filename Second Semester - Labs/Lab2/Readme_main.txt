{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 MAIN\
\
Il codice gira in circa 3 ore (credo si possa far girare pi\'f9 volte in contemporanea perch\'e9 una singola run usa solo una bassa percentuale del processore, quindi dovrebbero comunque finire in 3 ore)\
\
Obiettivo: ottenere grafici del service time per diverse situazioni (ogni risultato deve avere confidence intervals)\
\
SIMULAZIONI: \
1) con diversa LINK_CAPACITY dei server (per ora nel codice ci sono 10Gbps, 10Mbps e 10kbps, se ne possono aggiungere altre)\
2) con diverso numero dei server (il file Amazon_servers_stations contiene 52 server, Amazon_servers_stations2 ne contiene 16, se ne potrebbe creare ancora uno con 3 server (uno in Europa, uno in Asia, uno in America))\
3) con diversa MAX_REQ (ha senso?)\
\
1) \
-usare Amazon_servers_stations2 e MAX_REQ=10\
-\ul per ogni valore\ulnone  di LINK_CAPACITY ripetere simulazione almeno 5 volte (magari con diverso random_seed o mettendo il random seed che cambia con il tempo), salvare i risultati del service time su excel, calcolare valor medio e deviazione standard\
-creare grafico con i valori di LINK_CAPACITY sull\'92asse x e risultati service time sulle y (i risultati devono essere accompagnati dal confidence interval, cio\'e8 si deve vedere valor medio +/- deviazione standard, credo)\
\
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0
\cf0 2) \
-usare LINK_CAPACITY=10Mbps e MAX_REQ=10\
-\ul per ogni valore\ulnone  di numero di server ripetere simulazione almeno 5 volte (magari con diverso random_seed), salvare i risultati del service time su excel, calcolare valor medio e deviazione standard\
-creare grafico con il numero di servers sull\'92asse x e risultati service time sulle y (i risultati devono essere accompagnati dal confidence interval, cio\'e8 si deve vedere valor medio +/- deviazione standard, credo)\
\
3) (se vogliamo fare anche questa)\
-usare LINK_CAPACITY=10Mbps e Amazon_servers_stations2\
-\ul per ogni valore\ulnone  di MAX_REQ ripetere simulazione almeno 5 volte (magari con diverso random_seed), salvare i risultati del service time su excel, calcolare valor medio e deviazione standard\
-creare grafico con i valori di MAX_REQ sull\'92asse x e risultati service time sulle y (i risultati devono essere accompagnati dal confidence interval, cio\'e8 si deve vedere valor medio +/- deviazione standard, credo)}