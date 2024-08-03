from colorama import init, Fore, Style

class ColorPrint:
    @staticmethod
    def pr(color: str, input_text: str) -> None:
        init()

        color_mapping = {
            "error": Fore.RED,
            "warn": Fore.CYAN,
            "blue": Fore.BLUE,
            "info": Fore.GREEN,
        }

        color_code = color_mapping.get(color, Fore.WHITE)
        print(color_code + str(input_text) + Style.RESET_ALL)
