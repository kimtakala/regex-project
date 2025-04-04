"""
This is the main program.
"""

import os
import sys
from sys import stdout
from time import sleep

# Dynamically add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.services.shunting_yard.state_machine import StateMachine

# Define spacing for alignment
GUIDE_SPACING = 15
EXAMPLES_SPACING = 50

# define sleep times
WAIT = 0.2

GUIDE = (
    "\n=== KÄYTTÖOHJEET ===\n\n"
    + "=== PERUSMERKIT ===\n"
    + "{:<{spacing}}mikä tahansa merkki paitsi rivinvaihto (esim. 'a', '1', '@')\n".format(
        ".", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}mikä tahansa sana-merkki (a-z, A-Z, 0-9, _)\n".format(
        "\\w", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}mikä tahansa numero (0-9)\n".format("\\d", spacing=GUIDE_SPACING)
    + "{:<{spacing}}mikä tahansa välilyönti (esim. välilyönti, tabulaattori)\n".format(
        "\\s", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}mikä tahansa ei-sana-merkki\n".format("\\W", spacing=GUIDE_SPACING)
    + "{:<{spacing}}mikä tahansa ei-numero\n".format("\\D", spacing=GUIDE_SPACING)
    + "{:<{spacing}}mikä tahansa ei-välilyönti\n".format("\\S", spacing=GUIDE_SPACING)
    + "\n=== MERKKIJOUKOT ===\n"
    + "{:<{spacing}}mikä tahansa merkki a, b tai c\n".format("[abc]", spacing=GUIDE_SPACING)
    + "{:<{spacing}}mikä tahansa merkki paitsi a, b tai c\n".format("[^abc]", spacing=GUIDE_SPACING)
    + "{:<{spacing}}mikä tahansa merkki väliltä a ja g (a, b, c, ..., g)\n\n".format(
        "[a-g]", spacing=GUIDE_SPACING
    )
    + "\n=== ERIKOISMERKIT ===\n"
    + "{:<{spacing}}vastaa merkkijonoa, joka alkaa 'abc' ja päättyy 'abc'\n".format(
        "^abc$", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}sanan raja (esim. 'cat\\b' vastaa 'cat', mutta ei 'cats')\n".format(
        "\\b", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}ei-sanan raja (esim. 'cat\\B' vastaa 'cats', mutta ei 'cat')\n\n".format(
        "\\B", spacing=GUIDE_SPACING
    )
    + "\n=== ESCAPED MERKIT ===\n"
    + "{:<{spacing}}piste-merkki '.'\n".format("\\.", spacing=GUIDE_SPACING)
    + "{:<{spacing}}tähti-merkki '*'\n".format("\\*", spacing=GUIDE_SPACING)
    + "{:<{spacing}}kenoviiva '\\'\n".format("\\\\", spacing=GUIDE_SPACING)
    + "{:<{spacing}}sarkain (tabulaattori)\n".format("\\t", spacing=GUIDE_SPACING)
    + "{:<{spacing}}rivinvaihto\n".format("\\n", spacing=GUIDE_SPACING)
    + "{:<{spacing}}rivinpaluu\n".format("\\r", spacing=GUIDE_SPACING)
    + "{:<{spacing}}unicode-merkki 'A' (esim. '\\x41' vastaa 'A')\n".format(
        "\\x41", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}unicode-merkki © (esim. '\\u00A9' vastaa '©')\n".format(
        "\\u00A9", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}unicode-merkki 😀 (esim. '\\U0001F600' vastaa '😀')\n\n".format(
        "\\U0001F600", spacing=GUIDE_SPACING
    )
    + "\n=== RYHMÄT JA LOOKAROUND ===\n"
    + "{:<{spacing}}ryhmän kaappaus (esim. '(abc)' vastaa 'abc')\n".format(
        "(abc)", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}viittaus ryhmään #1 (esim. '(a)(b)\\1' vastaa 'aba')\n".format(
        "\\1", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}ei-kaappaava ryhmä (esim. '(?:abc)' vastaa 'abc', mutta ei tallenna ryhmää)\n".format(
        "(?:abc)", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}positiivinen lookahead (esim. 'a(?=b)' vastaa 'a' vain jos sitä seuraa 'b')\n".format(
        "(?=abc)", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}negatiivinen lookahead (esim. 'a(?!b)' vastaa 'a' vain jos sitä ei seuraa 'b')\n".format(
        "(?!abc)", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}positiivinen lookbehind (esim. '(?<=a)b' vastaa 'b' vain jos sitä edeltää 'a')\n".format(
        "(?<=abc)", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}negatiivinen lookbehind (esim. '(?<!a)b' vastaa 'b' vain jos sitä ei edeltänyt 'a')\n\n".format(
        "(?<!abc)", spacing=GUIDE_SPACING
    )
    + "\n=== TOISTOT ===\n"
    + "{:<{spacing}}0 tai enemmän 'a'-merkkejä (esim. 'a*' vastaa '', 'a', 'aa', ...)\n".format(
        "a*", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}1 tai enemmän 'a'-merkkejä (esim. 'a+' vastaa 'a', 'aa', ...)\n".format(
        "a+", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}0 tai 1 'a'-merkkiä (esim. 'a?' vastaa '', 'a')\n".format(
        "a?", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}tasan viisi 'a'-merkkiä (esim. 'a{{5}}' vastaa 'aaaaa')\n".format(
        "a{{5}}", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}vähintään kaksi 'a'-merkkiä (esim. 'a{{2,}}' vastaa 'aa', 'aaa', ...)\n".format(
        "a{{2,}}", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}välillä yksi ja kolme 'a'-merkkejä (esim. 'a{{1,3}}' vastaa 'a', 'aa', 'aaa')\n".format(
        "a{{1,3}}", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}ota mahdollisimman vähän 'a'-merkkejä (esim. 'a+?' vastaa 'a' ensimmäisenä)\n".format(
        "a+?", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}ota mahdollisimman vähän vähintään kaksi 'a'-merkkejä (esim. 'a{{2,}}?' vastaa 'aa')\n".format(
        "a{{2,}}?", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}vastaa joko 'ab' tai 'cd' (esim. 'ab|cd' vastaa 'ab' tai 'cd')\n".format(
        "ab|cd", spacing=GUIDE_SPACING
    )
    + "\n"
)

EXAMPLES = (
    "\n=== ESIMERKIT ===\n\n"
    + "{:<{spacing}}vastaa merkkijonoa, joka alkaa 'abc' ja päättyy 'xyz' (esim. 'abc123xyz')\n".format(
        "^abc.*xyz$", spacing=EXAMPLES_SPACING
    )
    + "{:<{spacing}}vastaa sähköpostiosoitetta (esim. 'user@example.com')\n".format(
        "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}", spacing=EXAMPLES_SPACING
    )
    + "{:<{spacing}}vastaa päivämäärää muodossa 'YYYY-MM-DD' (esim. '2023-10-01')\n".format(
        "\\d{4}-\\d{2}-\\d{2}", spacing=EXAMPLES_SPACING
    )
    + "{:<{spacing}}vastaa puhelinnumeroa muodossa '(123) 456-7890'\n".format(
        "\\(\\d{3}\\) \\d{3}-\\d{4}", spacing=EXAMPLES_SPACING
    )
    + "{:<{spacing}}vastaa URL-osoitetta (esim. 'https://example.com')\n".format(
        "https?://[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}(/\\S*)?", spacing=EXAMPLES_SPACING
    )
    + "{:<{spacing}}vastaa merkkijonoa, jossa on vain isoja kirjaimia (esim. 'HELLO')\n".format(
        "^[A-Z]+$", spacing=EXAMPLES_SPACING
    )
    + "{:<{spacing}}vastaa merkkijonoa, jossa on vähintään yksi numero (esim. 'abc123')\n".format(
        ".*\\d+.*", spacing=EXAMPLES_SPACING
    )
    + "{:<{spacing}}vastaa postinumeroa (esim. '12345' tai '12345-6789')\n".format(
        "\\d{5}(-\\d{4})?", spacing=EXAMPLES_SPACING
    )
    + "{:<{spacing}}vastaa merkkijonoa, jossa on vain pieniä kirjaimia ja numeroita\n".format(
        "^[a-z0-9]+$", spacing=EXAMPLES_SPACING
    )
    + "{:<{spacing}}vastaa merkkijonoa, joka ei sisällä välilyöntejä\n".format(
        "^\\S+$", spacing=EXAMPLES_SPACING
    )
    + "\n"
)


class Colors:
    """
    colors for UI
    """

    PETROL_GREEN = "\033[38;2;0;128;128m"
    LIGHT_GREEN = "\033[38;2;144;238;144m"
    DARK_ORANGE = "\033[38;2;255;140;0m"
    DARK_RED = "\033[38;2;139;0;0m"
    BRIGHT_YELLOW = "\033[38;2;255;255;0m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_title(title):
    """
    prints the title
    """
    sleep(WAIT)
    print(f"{Colors.PETROL_GREEN}\n{'=' * 40}{Colors.ENDC}")
    sleep(WAIT)
    print(f"{Colors.PETROL_GREEN}{title:^40}{Colors.ENDC}")
    sleep(WAIT)
    print(f"{Colors.PETROL_GREEN}{'=' * 40}{Colors.ENDC}")
    sleep(WAIT)


def print_guide():
    """
    prints the guide
    """
    print(f"\n{Colors.DARK_ORANGE}{'=' * 40}{Colors.ENDC}")
    print(f"{Colors.DARK_ORANGE}{'KÄYTTÖOHJEET':^40}{Colors.ENDC}")
    print(f"{Colors.DARK_ORANGE}{'=' * 40}{Colors.ENDC}")
    print(f"{Colors.BRIGHT_YELLOW}{GUIDE}{Colors.ENDC}")


def print_examples():
    """
    prints the examples
    """
    print(f"\n{Colors.DARK_ORANGE}{'=' * 40}{Colors.ENDC}")
    print(f"{Colors.DARK_ORANGE}{'ESIMERKIT':^40}{Colors.ENDC}")
    print(f"{Colors.DARK_ORANGE}{'=' * 40}{Colors.ENDC}")
    print(f"{Colors.BRIGHT_YELLOW}{EXAMPLES}{Colors.ENDC}")


def loop():
    """
    This is the main loop with two modes: regex mode and guide mode.
    """
    initial = True
    try:
        print(f"{Colors.PETROL_GREEN}\nkäynnistetään ohjelmaa", end="")
        stdout.flush()
        for _ in range(9):
            sleep(WAIT)
            print(".", end="")
            stdout.flush()
        print(f"{Colors.ENDC}")
        print_title("REGEX-SYNTAX-CHECKER 0.5")
        sleep(WAIT)
        print(f"{Colors.PETROL_GREEN}Tervetuloa RegEx-tarkistustyökaluun!{Colors.ENDC}")
        sleep(WAIT)
        print(
            f"{Colors.PETROL_GREEN}Tällä ohjelmalla voit tarkistaa säännöllisten lausekkeiden syntaksin,\n{Colors.ENDC}"
        )
        sleep(WAIT)
        print(f"{Colors.PETROL_GREEN}tutustua ohjeisiin ja nähdä esimerkkejä.{Colors.ENDC}")
        sleep(WAIT)
        print(
            f"{Colors.PETROL_GREEN}Voit vaihtaa tilojen välillä syöttämällä tyhjän rivin.\n{Colors.ENDC}"
        )

        current_mode = None  # Track the current mode: 'regex' or 'guide'

        while True:
            # Regex mode
            if current_mode != "regex":
                if initial:
                    sleep(WAIT)
                print(f"{Colors.PETROL_GREEN}\n=== SYNTAKSIN TARKISTUS TILA ==={Colors.ENDC}")
                if initial:
                    sleep(WAIT)
                print(
                    f"{Colors.PETROL_GREEN}Syötä säännöllinen lauseke tarkistaaksesi RegEx syntaksi.{Colors.ENDC}"
                )
                if initial:
                    sleep(WAIT)
                print(
                    f"{Colors.PETROL_GREEN}Jätä tyhjäksi siirtyäksesi ohje-tilaan.\n{Colors.ENDC}"
                )
                if initial:
                    sleep(WAIT * 3)
                print(f"{Colors.PETROL_GREEN}ohjelma ladattu onnistuneesti.\n{Colors.ENDC}")
                current_mode = "regex"
                if initial:
                    sleep(WAIT * 3)
                initial = False

            regex = input(f"{Colors.PETROL_GREEN}Syötä säännöllinen lauseke: {Colors.ENDC}")

            if regex:
                try:
                    sm = StateMachine(regex)
                    sm.tokenize()
                    print(
                        f'{Colors.LIGHT_GREEN}Syöte: "{regex}" noudattaa RegEx syntaksia!{Colors.ENDC}'
                    )
                except Exception as e:
                    print(
                        f'{Colors.DARK_RED}Syöte: "{regex}" ei noudata RegEx syntaksia. {Colors.ENDC}'
                    )
                    print(f"{Colors.DARK_RED}Virhe: {e}{Colors.ENDC}")
            else:
                # Guide mode
                if current_mode != "guide":
                    print(f"{Colors.DARK_ORANGE}\n=== OHJE TILA ==={Colors.ENDC}")
                    print(
                        f"{Colors.DARK_ORANGE}Syötä 'o' tulostaaksesi ohjeet, 'e' esimerkit, tai '.' sulkeaksesi ohjelman.{Colors.ENDC}"
                    )
                    print(
                        f"{Colors.DARK_ORANGE}Jätä tyhjäksi palataksesi regex-tarkistus-tilaan.{Colors.ENDC}"
                    )
                    current_mode = "guide"

                while True:
                    command = input(f"{Colors.DARK_ORANGE}\nSyötä komento: {Colors.ENDC}")

                    if command:
                        if command == "o":
                            print_guide()
                        elif command == "e":
                            print_examples()
                        elif command == ".":
                            print(
                                f"{Colors.DARK_ORANGE}Ohjelman suoritus päättyy... Moikka!{Colors.ENDC}"
                            )
                            sys.exit()
                        else:
                            print(
                                f'{Colors.DARK_RED}Virheellinen komento. Syötä "o", "e", "." tai tyhjä.{Colors.ENDC}'
                            )
                    else:
                        # Switch back to regex mode
                        current_mode = None
                        break

    except KeyboardInterrupt:
        if current_mode == "regex":
            color = Colors.PETROL_GREEN
        else:
            color = Colors.DARK_ORANGE
        print(f"\n{color}Ohjelman suoritus keskeytetty käyttäjän toimesta... Moikka!{Colors.ENDC}")


if __name__ == "__main__":
    loop()
