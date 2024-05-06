from colorama import init, Fore, Back, Style


class ColorPrint:
    @staticmethod
    def pr(color: str, input_text: str) -> None:

        init()
        if color == "error":
                print(Fore.RED + str(input_text))
        elif color == "warn":
                print(Fore.CYAN + str(input_text))
        elif color == "blue":
                print(Fore.BLUE + str(input_text))
        elif color == "info":
                print(Fore.GREEN + str(input_text))
        else:
                print(Fore.WHITE + str(input_text))
