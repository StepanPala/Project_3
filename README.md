# Elections Scraper

*Note: English follows*

Jednoduchý web scraper, kterým lze získat data z webu volby.cz.

## Popis

Program umožní extrahovat údaje z výsledků parlamentní voleb v roce [2017](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).
Umí získat kód a název obce, počet voličů v obci, vydané obálky a platné hlasy, dále pak všechny kandidující strany a počet získaných hlasů.
Údaje poté uloží do csv souboru se zvoleným názvem.

## Použité knihovny

Knihovny nutné ke spuštění programu jsou uvedeny v souboru `requirements.txt`.  
K instalaci externích knihoven je vhodné použít virtuální prostředí.  
Knihovny lze nainstalovat následovně:  
`pip install -r requirements.txt`

## Používání programu

Program se spouští příkazovým řádkem, a to zadáním dvou povinných argumentů, tedy:  
`python main.py "<odkaz_na_územní_celek>" "<název_výstupního_souboru>"`  
Výsledky se uloží do souboru s příponou `.csv`.

## Příklad fungování

Volební výsledky v územním celku Pardubice:

1. argument 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9&xnumnuts=5302'
2. argument 'vysledky_pardubice.csv'

Spuštění:

`python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9&xnumnuts=5302" "vysledky_pardubice.csv"`

Průběh:

```Extracting data from https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9&xnumnuts=5302...  
Data extracted successfully.  
Saving data to vysledky_pardubice.csv...  
Data saved successfully.  
Terminating Elections Scraper...
```

Ukázka výstupu:

```Code,Location,Registered,Envelopes,Valid,...  
574724,Barchov,170,113,113,5,0,0,9,0,12,7,0,3,1,0,0,14,0,3,40,0,1,3,0,0,0,15,0  
574741,Bezděkov,262,164,163,18,0,0,5,0,14,9,7,1,2,0,0,20,0,7,58,0,1,3,4,2,0,11,1  
...
```

## Autor
Štěpán Pala


# Elections Scraper

A simple web scraper for extracting data from volby.cz.

## Description

The program can extract data from the [2017](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) Czech parliament elections data.
It retrieves the code and name of individual locations, number of registered voters, issued envelopes and valid votes, as well as all the candidate parties and the number of the votes they received.
The data is then saved to a csv file using the name specified by the user.

## Dependencies

The packages necessary to run the program are specified in `requirements.txt`.  
A virtual environment is recommended to install external packages.  
The dependencies can be installed as follows:  
`pip install -r requirements.txt`

## Usage

To run the program, use the following arguments in the command line:  
`python main.py "<location_URL>" "<output_filename>"`  
The results are then saved to a `.csv` file.

## Example

Election results for Pardubice:

1. argument `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9&xnumnuts=5302`
2. argument `results_pardubice.csv`

Initiation:

`python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9&xnumnuts=5302" "results_pardubice.csv"`

Progress:

```Extracting data from https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9&xnumnuts=5302...  
Data extracted successfully.  
Saving data to results_pardubice.csv...  
Data saved successfully.  
Terminating Elections Scraper...
```

Output example:

```Code,Location,Registered,Envelopes,Valid,...  
574724,Barchov,170,113,113,5,0,0,9,0,12,7,0,3,1,0,0,14,0,3,40,0,1,3,0,0,0,15,0  
574741,Bezděkov,262,164,163,18,0,0,5,0,14,9,7,1,2,0,0,20,0,7,58,0,1,3,4,2,0,11,1  
...
```
