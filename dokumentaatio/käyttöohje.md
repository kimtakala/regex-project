# Käyttöohje

## Ohjelman asennus

lataa projekti omalle tietokoneelle:

```bash
git clone git@github.com:kimtakala/regex-project.git
```

siirry projektin juureen:

```bash
cd regex-project
```

asenna poetry:

```bash
pip install poetry
```

asenna riippuvuudet:

```bash
poetry install --no-root
```

## Ohjelman suorittaminen

suorita ohjelma komennolla:

```bash
poetry run python regex_program.py
```

## Ohjeet:

Kun ohjelma on käynnistynyt pääset lukemaan ohjeita ja näkemään esimerkkejä jättämällä tekstikentän tyhjäksi ja painamalla `enter` näppäintä.

Ohjetilassa näet kyseisen tilan ohjeet viestillä `o` ja esimerkit viestillä `e`, tilaa vaihdetaa viestillä `v`.

Näitä ei tarvitse muistaa ulkoa, käyttöliittymä ohjeistaa.

### Minkä muotoisia syötteitä ohjelma hyväksyy:

#### Yksinkertainen Regex Haku

Hyväksytään perusmerkit (a-z, A-Z, 0-9) ja erikoismerkit: ()|?\*+.

**Erikoismerkkien käyttö:**

| erikoismerkki | käyttö                                  | hyväksyttävät syötteet |
| ------------- | --------------------------------------- | ---------------------- |
| a\*           | a merkkiä on 0 tai enemmän              | (tyhjä), a, aa, ...    |
| a?            | a merkkiä on 0 tai 1                    | (tyhjä), a,            |
| a+            | a merkkiä on 1 tai enemmän              | a, aa, ...             |
| a\|b          | joko merkki a tai b                     | a, b                   |
| a.b           | Konkatenaatio merkki. Ensin a, sitten b | ab                     |
| (a\|b\|c)?    | Ryhmä merkintä                          | (tyhjä), a, b, c       |

#### Täydellinen regex syntaxin tarkistus

Tässä esimerkki kuva siitä millaista regexiä sillä voi tarkistaa, syötät haluamasi regex lausekkeen, se kertoo sinulle noudattaako se regexin syntaxia ja jos ei niin miksi ei.

![regex example image](https://github.com/kimtakala/regex-project/blob/main/dokumentaatio/kuvat/regular-expression.webp)
