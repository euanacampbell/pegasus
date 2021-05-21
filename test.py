from modules.generic.clipboard import Clipboard




clipboard = Clipboard.get_clipboard().splitlines()

master = [row.split('\t') for row in clipboard]
