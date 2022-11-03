import colorama
from colorama import Fore
from django.conf import settings


def print_colored_text(code, *styles):
    if settings.DEBUG:
        colorama.init()
        text_to_print = ""
        for style in styles:
            text_to_print += style
        text_to_print += str(code)
        print(f"{text_to_print}" + Fore.RESET)
