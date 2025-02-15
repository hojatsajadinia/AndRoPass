from colorama import init, Fore, Style
from typing import Dict, Optional

class ColorPrint:
    """Utility class for printing colored text to the console."""
    
    COLOR_MAP: Dict[str, str] = {
        "error": Fore.RED,
        "warn": Fore.YELLOW,  
        "blue": Fore.BLUE,
        "info": Fore.GREEN,
        "default": Fore.WHITE
    }
    
    @classmethod
    def pr(cls, color: str, input_text: str) -> None:
        """
        Print text in specified color.
        
        Args:
            color: Color identifier string (error/warn/blue/info)
            input_text: Text to be printed
        """
        init() 
        color_code = cls.COLOR_MAP.get(color.lower(), cls.COLOR_MAP["default"])
        print(f"{color_code}{input_text}{Style.RESET_ALL}")
