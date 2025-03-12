# Määrittelydokumentti

Tämä dokumentti määrittelee Helsingin Yliopiston Tietojenkäsittelytieteen kandiohjelman kevään 2025 4. periodin Aineopintojen Harjoitustyö: Algoritmit ja Tekoäly -kurssin projektin toteutuksen. Tämän dokumentaation kieli on suomi.

## Aihe

Aiheena on RegEx tulkin toteutus pythonilla. Ratkaisen projektillani ongelman regular expressioneiden, eli säännöllisten lausekkeiden tulkinnasta tehokkaasti. Harjoitustyön ydin on luoda tulkki joka pystyy käydä läpi annettun merkkijonon tehokkaasti ja kertoa, että noudattaako se RegEx sääntöjä, ja jos ei niin mitä sääntö se rikkoo. Ohjelma saa syötteenään merkkijonon, joka sisältää erikoismerkkejä, ohjelma analysoi merkkijonon ja kertoo mikä on sen toiminto RegEx syntaxin mukaisesti.

### Algoritmit ja tietorakenteet sekä, niiden aikavaativuudet:
#### Vaiheet:
1. Parsinta
    - Muunnetaan merkkijono shunting-yard algoritmillä postfix muotoon.
    - Aikavaativuus: ``O(n)``
2. Automaattinen Rakentaminen
    - Muunnetaan postfix muotoinen regex NFA:ksi Thompson's Construction algoritmilla.
    - Aikavaativuus: ``O(n)``
3. Matchaus
    - Thompsonin NFA-simulaatio käyttäen tila-joukkoa ja BFS-tyylistä etenemistä
    - Aikavaativuus: ``O(nm)``, missä ``n`` on NFA:n tilojen määrä ja ``m`` on syötteen pituus.
4. Virheiden selitys
    - Toteutetaan state tracking metodilla, jossa seurataan aktiivisesti syötteen käsittelyä ja kirjataan, missä kohtaa ja miksi syöte ei läpäise regexiä.
    - Aikavaativuus ``O(n)``

Kokonais aikavaativuus: ``O(nm)``

## Ohjelmointikielet

### Projekti:

Pääasiallisena ohjelmointikielenä toimii Python.

Yksikkötestaus toteutetaan pytestilla ja koodin muotoilu pylintilla.

### Vertaisarvioinnit:

Vertaisarvioinneissa kielenä voi olla pythonin lisäksi c++.

## Viitteet
[Shunting Yard Algorithm](https://en.wikipedia.org/wiki/Shunting_yard_algorithm)
[Postfix Notation](https://simple.wikipedia.org/wiki/Postfix_notation)
[Thompson's Construction](https://en.wikipedia.org/wiki/Thompson%2527s_construction)
[Nondeterministic Finite Automaton](https://en.wikipedia.org/wiki/Nondeterministic_finite_automaton)