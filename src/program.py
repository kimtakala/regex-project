"""
This is the main program with two regex modes:
1. Simple Regex Search (Primary mode using NFA implementation)
2. Perfect Regex Syntax Checker (Secondary mode)
"""

import os
import sys
from sys import stdout
from time import sleep

# Dynamically add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.services import matchRegex, EmptyRegexError, InvalidRegexError, RegexTokenizer

# Define spacing for alignment
GUIDE_SPACING = 15
EXAMPLES_SPACING = 50

# define sleep times
WAIT = 0.2

# Simple regex guide for NFA implementation
SIMPLE_GUIDE = (
    "\n=== KÄYTTÖOHJEET - YKSINKERTAINEN REGEX ===\n\n"
    + "=== PERUSMERKIT ===\n"
    + "{:<{spacing}}mikä tahansa merkki (esim. 'a', '1', '@')\n".format(
        "a,b,c...", spacing=GUIDE_SPACING
    )
    + "\n=== OPERAATTORIT ===\n"
    + "{:<{spacing}}yhdistää kaksi lauseketta (esim. 'a.b' vastaa 'a' ja sitten 'b')\n".format(
        ".", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}vastaa joko vasemmalla tai oikealla olevaa lauseketta (esim. 'a|b' vastaa 'a' tai 'b')\n".format(
        "|", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}0 tai enemmän toistoja (esim. 'a*' vastaa '', 'a', 'aa', ...)\n".format(
        "*", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}1 tai enemmän toistoja (esim. 'a+' vastaa 'a', 'aa', ...)\n".format(
        "+", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}0 tai 1 toistoa (esim. 'a?' vastaa '', 'a')\n".format(
        "?", spacing=GUIDE_SPACING
    )
    + "{:<{spacing}}ryhmittelyä varten (esim. '(a|b)c' vastaa 'ac' tai 'bc')\n".format(
        "()", spacing=GUIDE_SPACING
    )
    + "\n"
)

# Simple regex examples for NFA implementation
SIMPLE_EXAMPLES = (
    "\n=== ESIMERKIT - YKSINKERTAINEN REGEX ===\n\n"
    + "{:<{spacing}}vastaa 'a', 'aa', ...\n".format("aa*", spacing=EXAMPLES_SPACING)
    + "{:<{spacing}}vastaa 'aa', 'aba', 'abba', ...\n".format("ab*a", spacing=EXAMPLES_SPACING)
    + "{:<{spacing}}vastaa 'abd' tai 'acd'\n".format("ab|cd", spacing=EXAMPLES_SPACING)
    + "{:<{spacing}}vastaa 'abc', 'abbc', 'abbbc', ...\n".format("ab+c", spacing=EXAMPLES_SPACING)
    + "{:<{spacing}}vastaa 'a', 'b' tai 'c'\n".format("a|b|c", spacing=EXAMPLES_SPACING)
    + "{:<{spacing}}vastaa 'aa', 'ab', 'ba' tai 'bb'\n".format(
        "(a|b)(a|b)", spacing=EXAMPLES_SPACING
    )
    + "{:<{spacing}}vastaa 'ac' tai 'abc'\n".format("a(b)?c", spacing=EXAMPLES_SPACING)
    + "\n"
)

# Full regex guide
FULL_GUIDE = (
    "\n=== KÄYTTÖOHJEET - TÄYDELLINEN REGEX ===\n\n"
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

# Full regex examples
FULL_EXAMPLES = (
    "\n=== ESIMERKIT - TÄYDELLINEN REGEX ===\n\n"
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
    BLUE = "\033[38;2;65;105;225m"
    PURPLE = "\033[38;2;128;0;128m"
    BRIGHT_YELLOW = "\033[38;2;255;255;0m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_title(title, color=Colors.PETROL_GREEN):
    """
    prints the title
    """
    sleep(WAIT)
    print(f"{color}{'=' * 40}{Colors.ENDC}")
    sleep(WAIT)
    print(f"{color}{title:^40}{Colors.ENDC}")
    sleep(WAIT)
    print(f"{color}{'=' * 40}{Colors.ENDC}")
    sleep(WAIT)


def print_guide(simple_mode=True):
    """
    prints the guide for the current mode
    """
    if simple_mode:
        color = Colors.BLUE
        guide = SIMPLE_GUIDE
    else:
        color = Colors.DARK_ORANGE
        guide = FULL_GUIDE

    print(f"\n{color}{'=' * 40}{Colors.ENDC}")
    print(f"{color}{'KÄYTTÖOHJEET':^40}{Colors.ENDC}")
    print(f"{color}{'=' * 40}{Colors.ENDC}")
    print(f"{Colors.BRIGHT_YELLOW}{guide}{Colors.ENDC}")


def print_examples(simple_mode=True):
    """
    prints the examples for the current mode
    """
    if simple_mode:
        color = Colors.BLUE
        examples = SIMPLE_EXAMPLES
    else:
        color = Colors.DARK_ORANGE
        examples = FULL_EXAMPLES

    print(f"\n{color}{'=' * 40}{Colors.ENDC}")
    print(f"{color}{'ESIMERKIT':^40}{Colors.ENDC}")
    print(f"{color}{'=' * 40}{Colors.ENDC}")
    print(f"{Colors.BRIGHT_YELLOW}{examples}{Colors.ENDC}")


def loop():
    """
    This is the main loop with three modes:
    1. Simple regex search mode (NFA-based)
    2. Advanced regex syntax checker mode
    3. Guide mode
    """
    try:
        print(f"{Colors.BLUE}\nkäynnistetään ohjelmaa", end="")
        stdout.flush()
        for _ in range(9):
            sleep(WAIT)
            print(".", end="")
            stdout.flush()
        sleep(WAIT * 3)
        print(f"\n{Colors.BLUE}ohjelma ladattu onnistuneesti.{Colors.ENDC}")
        sleep(WAIT)
        print(f"{Colors.ENDC}")
        print_title("REGEX-TYÖKALU 1.0", Colors.BLUE)
        sleep(WAIT)
        print(f"{Colors.BLUE}Tervetuloa RegEx-työkaluun!\n{Colors.ENDC}")
        sleep(WAIT)
        print(f"{Colors.BLUE}Tällä ohjelmalla voit kokeilla säännöllisiä lausekkeita,{Colors.ENDC}")
        sleep(WAIT)
        print(f"{Colors.BLUE}tarkistaa syntaksia ja tutustua ohjeisiin.\n{Colors.ENDC}")
        sleep(WAIT)
        print(
            f"{Colors.BLUE}Sovelluksessa on kaksi tilaa: yksinkertainen ja täydellinen RegEx.{Colors.ENDC}"
        )

        # Set initial mode as simple regex (NFA-based)
        in_simple_mode = True  # True for simple regex mode, False for advanced regex syntax checker
        current_mode = "regex"  # 'regex' or 'guide'

        while True:

            # Show appropriate header based on mode
            if in_simple_mode and current_mode == "regex":
                color = Colors.BLUE
                mode_name = "YKSINKERTAINEN REGEX HAKU"
                instruction = "Syötä säännöllinen lauseke ja teksti etsiäksesi vastaavuuksia."
            elif not in_simple_mode == "regex":
                color = Colors.PETROL_GREEN
                mode_name = "TÄYDELLINEN REGEX SYNTAKSIN TARKISTUS"
                instruction = "Syötä säännöllinen lauseke tarkistaaksesi RegEx syntaksi."
            else:  # guide
                color = Colors.DARK_ORANGE

            if current_mode == "regex":
                print(f"\n{color}=== {mode_name} ==={Colors.ENDC}")
                print(f"{color}{instruction}{Colors.ENDC}")
                print(f"{color}Jätä tyhjäksi siirtyäksesi ohje-tilaan.{Colors.ENDC}")
                print(f"{color}Syötä 'vaihda' vaihtaaksesi regex-tilaa.{Colors.ENDC}")

            if in_simple_mode and current_mode == "regex":
                # Simple Regex Mode (NFA-based)
                regex = input(f"{Colors.BLUE}Syötä säännöllinen lauseke: {Colors.ENDC}")

                if not regex:
                    current_mode = "guide"
                    continue
                elif regex.lower() == "vaihda":
                    in_simple_mode = False
                    print(
                        f"{Colors.PETROL_GREEN}Vaihdettu täydelliseen regex-syntaksitilaan.{Colors.ENDC}"
                    )
                    continue

                # Ask for text to match against
                text = input(f"{Colors.BLUE}Syötä testattava teksti: {Colors.ENDC}")

                try:
                    # Use the matchRegex function from nfa.py
                    result = matchRegex(regex, text)
                    if result:
                        print(
                            f"{Colors.PURPLE}Teksti '{text}' vastaa lauseketta '{regex}'!{Colors.ENDC}"
                        )
                    else:
                        print(
                            f"{Colors.DARK_RED}Teksti '{text}' ei vastaa lauseketta '{regex}'.{Colors.ENDC}"
                        )
                except (EmptyRegexError, InvalidRegexError) as e:
                    print(f"{Colors.DARK_RED}Virheellinen regex: {e}{Colors.ENDC}")
                    print(
                        f"{Colors.BRIGHT_YELLOW}Muistithan käyttää konkatenaatio operaattoria '.'?{Colors.ENDC}"
                    )
                except Exception as e:
                    print(f"{Colors.DARK_RED}Virhe: {e}{Colors.ENDC}")
                    print(
                        f"{Colors.BRIGHT_YELLOW}Muistithan käyttää konkatenaatio operaattoria '.'?{Colors.ENDC}"
                    )

            elif not in_simple_mode and current_mode == "regex":
                # Perfect Regex Syntax Mode
                regex = input(f"{Colors.PETROL_GREEN}Syötä säännöllinen lauseke: {Colors.ENDC}")

                if not regex:
                    current_mode = "guide"
                    continue
                elif regex.lower() == "vaihda":
                    in_simple_mode = True
                    print(f"{Colors.BLUE}Vaihdettu yksinkertaiseen regex-hakutilaan.{Colors.ENDC}")
                    continue

                try:
                    RegexTokenizer(regex)
                    print(
                        f'{Colors.LIGHT_GREEN}Syöte: "{regex}" noudattaa RegEx syntaksia!{Colors.ENDC}'
                    )
                except Exception as e:
                    print(
                        f'{Colors.DARK_RED}Syöte: "{regex}" ei noudata RegEx syntaksia. {Colors.ENDC}'
                    )
                    print(f"{Colors.DARK_RED}Virhe: {e}{Colors.ENDC}")

            # Guide mode
            while current_mode == "guide":
                print(f"\n{Colors.DARK_ORANGE}=== OHJE TILA ==={Colors.ENDC}")
                print(
                    f"{Colors.DARK_ORANGE}Syötä 'o' tulostaaksesi ohjeet, 'e' esimerkit, 'vaihda' vaihtaaksesi regex-tilaa, tai '.' sulkeaksesi ohjelman.{Colors.ENDC}"
                )
                print(f"{Colors.DARK_ORANGE}Jätä tyhjäksi palataksesi regex-tilaan.{Colors.ENDC}")

                command = input(f"{Colors.DARK_ORANGE}\nSyötä komento: {Colors.ENDC}")

                if command:
                    if command == "o":
                        print_guide(in_simple_mode)
                    elif command == "e":
                        print_examples(in_simple_mode)
                    elif command == "vaihda":
                        in_simple_mode = not in_simple_mode
                        mode_str = "yksinkertaiseen" if in_simple_mode else "täydelliseen"
                        print(
                            f"{Colors.DARK_ORANGE}Vaihdettu {mode_str} regex-tilaan.{Colors.ENDC}"
                        )
                    elif command == ".":
                        print(
                            f"{Colors.DARK_ORANGE}Ohjelman suoritus päättyy... Moikka!{Colors.ENDC}"
                        )
                        sys.exit()
                    else:
                        print(
                            f'{Colors.DARK_RED}Virheellinen komento. Syötä "o", "e", "vaihda", "." tai tyhjä.{Colors.ENDC}'
                        )
                else:
                    # Switch back to regex mode
                    current_mode = "regex"
                    break

    except KeyboardInterrupt:
        if in_simple_mode:
            color = Colors.BLUE
        elif current_mode == "regex":
            color = Colors.PETROL_GREEN
        else:
            color = Colors.DARK_ORANGE
        print(f"\n{color}Ohjelman suoritus keskeytetty käyttäjän toimesta... Moikka!{Colors.ENDC}")


if __name__ == "__main__":
    loop()
