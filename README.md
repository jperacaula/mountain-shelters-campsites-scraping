# Pràctica 1 - Tipologia i cicle de vida de les dades

Assignatura: M2.851 / Semestre: 2022-1 / Data: 22-11-2022

URL del lloc web triat: https://www.walkaholic.me/

## Autors
  * Sara Jose Roig - [sjoser@uoc.edu](sjoser@uoc.edu)
  * Joan Peracaula Prat - [joanperacaula@uoc.edu](joanperacaula@uoc.edu)

## Descripció

En aquesta pràctica hem escollit crear un dataset de llocs on dormir a la muntanya, siguin refugis (lliures o guardats) o bé espais d’acampada habilitats, en les regions d’Espanya, Andorra i sud de França. 

El lloc web d’on s’ha extret aquesta informació és https://www.walkaholic.me/. Aquesta es tracta d’una plataforma encarada als amants del senderisme, amb rutes i allotjaments (refugis i llocs d’acampada) a Espanya, Andorra i França. 

## Estructura del projecte 

 - `memoria.pdf`: Document memòria del projecte, amb les respostes de l'enunciat. 
 - `LICENSE`: Llicència del projecte, The MIT License.   
 - `/source`: Directori amb el codi utilitzat pel web scraping i creació del dataset. 
   - `/source/requirements.txt`: Fitxer amb les dependències necessàries per executar el codi. 
   - `/source/main.py`: Fitxer python punt d'entrada al programa. Inicia el web scraping i finalment guarda les dades. 
   - `/source/scraper.py`: Fitxer python que s'encarrega, principalment, de fer les requests a la pàgina web. Conté dues funcions: una per extreure tots els enllaços als allotjaments i una altra que recorre els enllaços i extreu les característiques de cada allotjament. 
   - `/source/accommodation_scraper.py`: Fitxer python que mitjançant diferents funcions extreu tots els atributs d'un allotjament. 
 - `/dataset`: Directori amb el dataset resultant. 
   - `/dataset/shelters_and_campsites.csv`: Fitxer CSV que conté totes les dades scrapejades.
 
## Dataset 

El dataset obtingut s'ha publicat a la plataforma Zenodo amb DOI [10.5281/zenodo.7338336](https://doi.org/10.5281/zenodo.7338336).

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7338336.svg)](https://doi.org/10.5281/zenodo.7338336)

## Video de presentació 

Enllaç al vídeo de presentació de la pràctica: [https://drive.google.com/...](https://drive.google.com/...)
