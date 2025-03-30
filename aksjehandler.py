#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 13:52:09 2023

@author: saraislaalvestad

Sindre Finnes sine aksjehandler
"""
import csv
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
import numpy as np
import yfinance as yf

filnavn="aksjehandler.csv"
datoer=[]
selskaper=[]
kurs=[]

with open(filnavn, 'r') as fil:
    innhold=csv.reader(fil, delimiter=",")
    overskrift= next(innhold)
    for rad in innhold:
        datoer.append(rad[2])
        selskaper.append(rad[4])
        kurs.append(rad[6])
 
# Funksjon som plotter grafer og diagrammer
def grafer(xakse,yakse,tittel):
    plt.xlabel(xakse)
    plt.ylabel(yakse)
    plt.title(tittel)
    plt.grid()
    plt.show()
    
    return(grafer)

# Mest og minst vanlige ukedag finnes handlet på
ukedager = [datetime.strptime(dato, "%d.%m.%Y").strftime("%A") for dato in datoer]
# %A returnerer ukedagen til datoen
ukedag_counter = Counter(ukedager)
# Går gjennom alle elementene i listen og plasserer de like sammen
mest_vanlige_ukedag, antall_ganger_mest = ukedag_counter.most_common()[0]
minst_vanlige_ukedag, antall_ganger_minst = ukedag_counter.most_common()[-1]
print(f"Finnes´ most common weekday to buy stocks was on  {mest_vanlige_ukedag}s with {antall_ganger_mest} trades.")
print(f"Finnes´ least common weekday to buy stocks was on  {minst_vanlige_ukedag}s with {antall_ganger_minst} trades.")

# Søylediagram som viser hvor mye aksjer som ble handlet på ulike ukedager
#Fjerner lørdag og søndag fordi børsen er stengt da
ukedag_counter.pop("Saturday", None)
ukedag_counter.pop("Sunday", None)
ukedager_rekkefølge = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
hverdager = [ukedag for ukedag in ukedager_rekkefølge]
antall_forekomster = [ukedag_counter[ukedag] for ukedag in hverdager]
farger = ['r', 'g', 'b', 'c', 'm']

plt.figure(figsize=(10, 6))
plt.bar(hverdager, antall_forekomster, color=farger)
plt.ylim(500, 750)
grafer("Ukedag", "Antall handler", "Antall handler fordelt på ukedager")

# Alle aksjehandlene fordelt på de 8 årene

handler_per_år = {}

# Legg til antall handler for hver dato i dictionary
for dato in datoer:
    år = datetime.strptime(dato, '%d.%m.%Y').year
    handler_per_år[år] = handler_per_år.get(år, 0) + 1
# Beregn totalt antall handler
totalt_antall = sum(handler_per_år.values())
# Legg til totalt antall i dictionary
handler_per_år['Totalt'] = totalt_antall

print("Aksjehandlene fordelt på år:")
for år, antall in handler_per_år.items():
    print(f"{år}: {antall}")

# Finnes sitt mest handlede selskap
selskaper_counter=Counter(selskaper)
mest_vanlige_selskap, antall_ganger = selskaper_counter.most_common()[0]
print(f"Selskapet finnes handlet mest i var {mest_vanlige_selskap} med {antall_ganger} handler.")

# Finnes sine 10 mest handlede selskaper
selskapsli = []
antallgangerli = []

for i in range(10):
    mest_vanlige_selskap, antall_ganger = selskaper_counter.most_common()[0]
    selskapsli.append(mest_vanlige_selskap)
    antallgangerli.append(antall_ganger)
    del selskaper_counter[mest_vanlige_selskap]

plt.barh(selskapsli, antallgangerli)
grafer("Selskaper", "Antall kjøp", "Mest handlede selskaper")

# Graf som plotter kursen til Q-free-aksjen hver gang finnes handlet den
# og tar en lineær regresjon som viser hvordan kursen endret seg
def linRegresjon(x, y):
    x = np.array(x)  # Konverter til NumPy-array
    reg = np.polyfit(x, y, 1)
    return reg[0] * x + reg[1]

datoerQfree = []
kursQfree = []

# Iterer over data for Q - FREE og legg til datoer og kurs i respektive lister
for i, selskap in enumerate(selskaper):
    if selskap == 'Q - FREE':
        dato = datoer[i]
        kurs_verdi = kurs[i].replace(',', '.')
        
        # Sjekk om kurs_verdi er en gyldig flyttall
        if kurs_verdi:
            datoerQfree.append(datetime.strptime(dato, '%d.%m.%Y'))
            kursQfree.append(float(kurs_verdi))

#Gjør datoene om til dager siden start for å gjøre regresjon            
startdato = datoerQfree[0]
dager_siden_start = [(dato - startdato).days for dato in datoerQfree]

# Utfør lineær regresjon for å finne trenden til kursen
forventet_y = linRegresjon(dager_siden_start, kursQfree)

# Plott de faktiske verdiene og den forutsagte linjen
plt.figure(figsize=(12, 6))
plt.scatter(datoerQfree, kursQfree, marker='o', color='blue', label='Kurs')
plt.plot(datoerQfree, forventet_y, color='red', label='Trend')
plt.legend()
grafer("Datoe", "Kurs", "Trenden til kursen til aksjen Q - FREE over tid")
# Bruker yfinance tilø å finne Q-frees faktiske kurs over den samme tidsperioden
symbol = 'QFR.OL'
start_dato = '2013-09-30'
slutt_dato = '2021-10-14'

# Henter historiske aksjekurser
data = yf.download(symbol, start=start_dato, end=slutt_dato)

plt.figure(figsize=(12, 6))
data['Adj Close'].plot(label=f'{symbol} Kurs')
plt.legend()
grafer("Dato", "Kurs", f'Kursen til aksjen til Q-FREE i perioden {start_dato} - {slutt_dato}')

# Finner antall bull og bearaksjer som ble handlet av finnes
bull = []
bear = []
bearDato = []

#Bruker enumerate for å på en enklere måte få riktig daoformat i bearDato
for i, selskap in enumerate(selskaper):
    if "BULL" in selskap:
        bull.append(selskap)
    elif "BEAR" in selskap:
        bear.append(selskap)
        bearDato.append(datetime.strptime(datoer[i], "%d.%m.%Y"))

print(f"Under Ernas statsministerperiode gjorde Finnes til sammen {len(bull)} bull-handler og {len(bear)} bear-handler")

# Finner antall bear-aksjer som ble handlet i 2020
start_dato = datetime(2020, 1, 1)
slutt_dato = datetime(2020, 12, 31)
mellomliggende_datoer = [dato for dato in bearDato if start_dato <= dato <= slutt_dato]
print(f"Under coronapandemien mellom {start_dato.strftime('%d.%m.%Y')} og {slutt_dato.strftime('%d.%m.%Y')}, handlet Finnes bear-aksjer {len(mellomliggende_datoer)} ganger.")
