
from pegasus.pegasus import Pegasus

while True:
    text_input = input('\ncommand: ')

    p = Pegasus().run_command(text_input)
