import time
import sys
import random
import pyfiglet
from colorama import Fore, Style, init
from termcolor import colored
# from banner.banner import print_mixed_colors_spider

# Initialisation de Colorama
init(autoreset=True)

# Fonction pour générer la bannière ASCII

def print_mixed_colors_spider(twinkling_duration=8):
    spider = [
        '    / _ \\ ',
        '  \\_\\(_)/_/',
        '   _//""\\_',
        '    /   \\  '
    ]

    # Liste de couleurs
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.LIGHTMAGENTA_EX, Fore.WHITE, Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX, Fore.MAGENTA, Fore.LIGHTWHITE_EX, Fore.LIGHTBLACK_EX]

    start_time = time.time()

    while time.time() - start_time < twinkling_duration:
        for line in spider:
            colored_line = ''
            for char in line:
                colored_line += random.choice(colors) + char + Style.RESET_ALL
            print(colored_line)
        sys.stdout.flush()
        time.sleep(0.1)
        print("\033c", end="")  # Clear screen

def generate_banner(text):
    ascii_banner = pyfiglet.figlet_format(text)
    return ascii_banner

# Liste de couleurs pour le scintillement
colors = [
    'red', 'yellow', 'green', 'cyan', 'blue', 
    'magenta', 'white', 'light_red', 'light_yellow',
    'light_green', 'light_cyan', 'light_blue', 'light_magenta'
]

# Fonction pour afficher la bannière avec un effet de scintillement coloré et rapide
def twinkling_banner(banner_text, twinkling_duration=5):
    start_time = time.time()
    ascii_banner = generate_banner(banner_text)

    while time.time() - start_time < twinkling_duration:
        colored_text = ""
        for char in ascii_banner:
            if char.strip():  # Ne colorie que les caractères non vides
                colored_text += colored(char, random.choice(colors))
            else:
                colored_text += char
        print(colored_text, end="\r")
        sys.stdout.flush()
        time.sleep(0.02)  # Réduction du temps de pause pour plus de rapidité
        print("\033c", end="")  # Efface l'écran pour donner un effet d'animation frénétique

# Fonction pour afficher un texte avec un effet de scintillement rapide
def twinkling_text(text, twinkling_duration=2):
    start_time = time.time()

    while time.time() - start_time < twinkling_duration:
        colored_text = [colored(char, random.choice(colors)) for char in text]
        sys.stdout.write(''.join(colored_text) + "\r")
        sys.stdout.flush()
        time.sleep(0.05)  # Réduction du temps de pause pour un effet plus rapide

    print('')

def fun_prompt():
    twinkling_banner("XSS Test", twinkling_duration=2)
    print_mixed_colors_spider(twinkling_duration=2)
    twinkling_text("Test XSS par TRHACKNON", twinkling_duration=2)
print(colored("Bienvenue sur l'outil de test XSS interactif modifié par ×TRHACKNON×", 'blue'))
if __name__ == "__main__":
    fun_prompt()