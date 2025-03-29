# Viikko 2

### Vastaa kysymyksiin:

#### Mitä olen tehnyt tällä viikolla?

- Coverage raportti luotu
- Testausta lisätty.
- Shunting-Yard algoritmin kehitys edennyt paljon [state_machine.py](../../src/services/shunting_yard/state_machine.py) hyvällä mallilla.
- [Pääohjelman](../../src/program.py) prototyyppi toimiva.

#### Miten ohjelma on edistynyt?

- Shunting-Yard algoritmin kehitys edennyt hyvin.
- StateMachine Tokenisaatio lähes valmis.

#### Mitä opin tällä viikolla / tänään?

- Tällä viikolla opin käyttämään iteraattoreita while true loopin sisällä, kutsumalla Next() funktiota.
- Näin syötteen käsittely toimii hyvin vaikka klassin funktiot kutsuvat toisiaan.

#### Mikä jäi epäselväksi tai tuottanut vaikeuksia?

- For looppien kanssa oli vaikeuksia iteraattoreiden käytössä, mutta ratkaisuksi löytyi while true, next kombo.

#### Mitä teen seuraavaksi?

- Viimeistelen StateMachinen.
- Siirryn Shunting-Yard algoritmin seuraaviin osiin.
  - Lisään implisiittisen konkatenaatio merkin.
    - §
  - Käsittelen ryhmä, lookaround, ja kvanttori tilanteet
    - (), {}, \*, +, ?
-  lisään testausta.
-  viimeistelen tokenisaation ja toteutan postfix muodon.

#### Käytetyt tunnit:

| **Päivä**     | **Käytetty aika** | **Kuvaus**                                                                  |
| ------------- | ----------------- | --------------------------------------------------------------------------- |
| 26.3.         | 2h               | escape sequence toteutus |
| 27.3.         | 6,5h               | escape sequence toteutus, square bracket toteutus, testaus toteutus |
| 29.3.         | 1,5h               | testaus toteutus, dokumentaatio |
| **Yhteensä:** | **10h**           |                                                                             |
