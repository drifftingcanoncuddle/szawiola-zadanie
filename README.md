# Symulacja rozprezania gazu doskonalego
Sposob uzycia:
1. Ustaw wlasciwosci symulacji w pliku `config.ini`
--1. Alternatywnie ustaw plik zawierajacy dane o czasteczkach
2. Uruchom generacje symulacji (flaga `-s`)
3. Uruchom generacje odpowiedniej animacji / wykresu (flagi `-etpv`)

W przypadku uszkodzenia pliku `config.ini` mozna przywrocic go do stanu poczatkowego uzywajac flagi `-r`
W przypadku dalszych problemow mozna uzyc flagi `-h`, aby zobaczyc pomoc

``` bash
python3 main.py [-h | -s | -t | -e | -v | -p | -f]
```
