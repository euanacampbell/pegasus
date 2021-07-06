import pyperclip

class Clipboard:

    def get_clipboard():
        return(pyperclip.paste())

    def add_to_clipboard(value):
        pyperclip.copy(value)