from services.shunting_yard.state_machine import StateMachine

GUIDE = """\
Merkkiluokat:
.	        mikä tahansa merkki paitsi rivinvaihto
\\w \\d \\s	sana, numero, välilyönti (word, digit, whitespace)
\\W \\D \\S	ei sana, numero, välilyönti
[abc]	        mikä tahansa a, b tai c
[^abc]	        ei a, b tai c
[a-g]	        merkki väliltä a ja g

Ankkurit:
^abc$	        merkkijonon alku / loppu
\\b	        sanan raja (word boundary)

Erikoismerkit:
\\. \\* \\\\	erikoismerkit
\\t \\n \\r	sarkain, rivinvaihto, rivinpaluu (tab, linefeed, carriage return)
\\u00A9	        unicode-merkki ©

Ryhmittely ja lookaround:
(abc)	        ryhmän kaappaus
\\1	        viittaus ryhmään #1
(?:abc)	        ei-kaappaava ryhmä
(?=abc)	        positiivinen lookahead
(?!abc)	        negatiivinen lookahead
(?<=abc)        positiivinen lookbehind
(?<!abc)        negatiivinen lookbehind

Kvanttorit ja Vaihtoehdot:
a* a+ a?	0 tai enemmän, 1 tai enemmän, 0 tai 1
a{{5}} a{{2,}}	tasan viisi, kaksi tai enemmän
a{{1,3}}	        välillä yksi ja kolme
a+? a{{2,}}?	ota mahdollisimman vähän
ab|cd	        vastaa ab tai cd \
"""


def loop():
    while True:
        regex = input(
            f"Syötä säännöllinen lauseke tarkistaaksesi RegEx, tai jätä tyhjäksi päästäksesi ohjeisiin: "
        )

        if regex:
            sm = StateMachine(regex)
            sm.tokenize()
            print(sm.tokens)
        else:
            print(f"{GUIDE}")


if __name__ == "__main__":
    loop()
