# Testausdokumentti

Tämä dokumentti määrittelee Helsingin Yliopiston Tietojenkäsittelytieteen kandiohjelman kevään 2025 4.
periodin Aineopintojen Harjoitustyö: Algoritmit ja Tekoäly -kurssin projektin testauksen.

[![GitHub CI](https://github.com/kimtakala/regex-project/actions/workflows/github_CI.yml/badge.svg)](https://github.com/kimtakala/regex-project/actions)
[![Codecov](https://codecov.io/github/kimtakala/regex-project/graph/badge.svg?token=J0KEHXVSRQ)](https://codecov.io/github/kimtakala/regex-project)

Projektin koodi on yksikkötestattu pytestillä ja codecovilla.

Testit löytyvät projektin juuresta 'tests'-[kansiosta](https://github.com/kimtakala/regex-project/tree/main/tests).

Kaikkiin mahdollisiin syötteisiin ollaan yritetty valmistautua ja se näkyy testauksen laajuudessa ja kattavuudessa.

Esimerkiksi täydellisen regexin syntaxin tarkistuksessa on quantifier braces eli "{}"
kohdalla 20 eri testiä, varmistamaan että kaikki uniikit virheet havaitaan testeillä.
Esimerkkejä näistä testeistä:

| Column 1 | Column 2 |
|----------|----------|
| Row 1    |       a   |
| Row 2    |         a |
| Row 3    |     a     |
| Row 4    |      a    |
| Row 5    |      a    |


Testit voidaan toistaa virtuaalisen ympäristön sisältä komennolla:
`pytest`
