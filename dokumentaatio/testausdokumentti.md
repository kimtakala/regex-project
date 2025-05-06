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

| rakenne | syy                                          |
| ------- | -------------------------------------------- |
| a{}     | tyhjä ei sallittu                            |
| a{1,a}  | vain numerot sallittu                        |
| {1,3}   | edeltävä merkki on pakollinen                |
| ${1,3}  | edeltävän merkin on oltava sallittua tyyppiä |
| a{1,3   | sulkeet on suljettava                        |

Testit voidaan toistaa virtuaalisen ympäristön sisältä komennolla:
`pytest`
