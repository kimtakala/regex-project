# Testausdokumentti

Tämä tiedosto on vielä työn alla...

Tämä dokumentti määrittelee Helsingin Yliopiston Tietojenkäsittelytieteen kandiohjelman kevään 2025 4. periodin Aineopintojen Harjoitustyö: Algoritmit ja Tekoäly -kurssin projektin testauksen.

## Kattavuus raportti:

| File                                      | Stmts | Miss | Cover | Missing                                  |
|-------------------------------------------|-------|------|-------|------------------------------------------
| src/\_\_init__.py                           | 1     | 0    | 100%  | -                                        |
| src/program.py                            | 12    | 12   | 0%    | 1-54                                     |
| src/services/\_\_init__.py                  | 1     | 0    | 100%  | -                                        |
| src/services/shunting_yard/\_\_init__.py    | 1     | 0    | 100%  | -                                        |
| src/services/shunting_yard/state_machine.py | 120   | 28   | 77%   | 89-122, 183, 228, 239-241, 283-289, 306, 312 |
| src/tests/\_\_init__.py                     | 0     | 0    | 100%  | -                                        |
| src/tests/test_state_machine.py           | 51    | 1    | 98%   | 129                                      |
| **TOTAL**                                 | 186   | 41   | 78%   | -                                        |

## Pylint score:

Your code has been rated at 9.64/10

## Mitä on Testattu ja miten?

### state_machine.py

testattu tiedostolla test_state_machine.py

Laaja kirjo syötteitä testaamaan tämän hetkistä implementaatiota, myöhemmin lisätään lisää testejä.

---

Miten testit voidaan toistaa?
