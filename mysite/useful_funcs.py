import colorama
from colorama import Back, Fore, Style


def print_colored_text(code, *styles):
    colorama.init()
    text_to_print = ""
    for style in styles:
        text_to_print += style
    text_to_print += str(code)
    print(f"{text_to_print}" + Fore.RESET, Back.RESET, Style.RESET_ALL)
