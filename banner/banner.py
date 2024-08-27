import time
import sys
import random
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize Colorama

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

def twinkling_text(text, twinkling_duration=2):
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.LIGHTMAGENTA_EX, Fore.WHITE, Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX, Fore.MAGENTA, Fore.LIGHTWHITE_EX, Fore.LIGHTBLACK_EX]

    start_time = time.time()

    while time.time() - start_time < twinkling_duration:
        colored_text = [random.choice(colors) + char + Style.RESET_ALL for char in text]
        sys.stdout.write(''.join(colored_text) + "\r")
        sys.stdout.flush()
        time.sleep(0.1)

    print('')

def fun_prompt():
    print(Fore.CYAN + "Bienvenue sur l'outil de test XSS interactif modifié par TRHACKNON")
    print_mixed_colors_spider(twinkling_duration=10)
    twinkling_text("Test XSS par TRHACKNON", twinkling_duration=4)