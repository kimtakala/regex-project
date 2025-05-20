# Toteutusdokumentti

### Ohjelman rakenne

Ohjelmassa on kaksi osaa.

1. Yksinkertaistettu regex haku
2. "Täydellinen" regexin syntaksin tarkistus

#### Yksinkertaistettu Regex Haku

Tässä tilassa ohjelmaan syötetään yksinkertaistetulla regex syntaxilla ensin regex ja sitten teksti.
Ohjelma tarkistaa matchaako regex syötteeseen.

#### "Täydellinen" Regex Syntaksin Tarkistus

Tässä tilassa ohjelmaan syötetään autenttinen regex lauseke,
ja ohjelma kertoo noudattaako se regex syntaxia ja jos ei, se antaa virhetiedot.

#### Lisäominaisuudet

Molemmissa tiloissa on myös pääsy ohjetilaan jossa on mahdollisuus tulostaa käyttöohjeet tai esimerkkejä.

### Aikavaativuudet

#### Yksinkertaistettu Regex Haku

Shunting Yard: O(n) missä n on syötteen pituus.

Compile Regex: O(n) missä n on postfixin pituus.

Match Regex: O(n^2) missä n on NFA:n tilojen määrä. (suhteellinen syötteen pituuteen)

Follow Epsilon states: O(n) missä n on NFA:n tilojen määrä.

#### "Täydellinen" Regex Syntaksin Tarkistus

Tokenize: O(n) missä n on syötteen pituus.

### Puutteet ja Parannusehdotukset

Ohjelmaa voisi kehittää tekemällä yksinkertaistetusta regexin tarkistuksesta
ja matchauksesta todellisen regexin syntaxin mukaisen.
Tämä olisi hyvin aikaa vievää, mutta mahdollista.

### Laajojen kielimallien käyttö

ChatGPT:tä on käytetty ohjelman UI:ssa olevan tekstin muotoiluun sekä kommenttien / docstringien luonnin tukena.
Sitä on myös käytetty lähteiden etsinnässä. Jos testi ei toiminut sitä on käytetty virheiden selittämiseen.
Laajoja kielimalleja ei ole käytetty koodin luontiin.

### Lähteet:

https://docs.python.org/3/library/re.html

https://en.wikipedia.org/wiki/Thompson%27s_construction

https://www.regexpal.com/

https://rosettacode.org/wiki/McNaughton-Yamada-Thompson_algorithm
