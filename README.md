# Symulacja rozprezania gazu doskonalego
Sposob uzycia:
1. Ustaw wlasciwosci symulacji w pliku `config.ini`. Alternatywnie ustaw plik zawierajacy dane o czasteczkach
2. Uruchom generacje symulacji (flaga `-s`)
3. Uruchom generacje odpowiedniej animacji / wykresu (flagi `-etpv`)

W przypadku uszkodzenia pliku `config.ini` mozna przywrocic go do stanu poczatkowego uzywajac flagi `-r`
W przypadku dalszych problemow mozna uzyc flagi `-h`, aby zobaczyc pomoc

## Skladnia w terminalu

``` bash
python3 main.py [-h | -s | -t | -e | -v | -p | -f]
```

## Wymogi pliku z pkt. 1
Plik powinien posiadać rosrzerzenie `.csv` i w jednej linijce powinien posiadac dane jednej czasteczki, ktore powinny byc sformatowane w nastepujacy sposob:
`polozenie_x, polozenie_y, predkosc_x, predkosc_y`
Program nie jest czuly na wystepowanie spacji pomiedyz wartosciami a przecinkiem
