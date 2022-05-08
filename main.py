import sys
from pegasus_client.pegasus import web, terminal

try:
    run_type = sys.argv[1]
except IndexError:
    run_type = input('Run type (web or terminal): ')

if run_type == 'web':
    peg = web()
elif run_type == 'terminal':
    peg = terminal()
else:
    print('run type not recognised')
    sys.exit()

peg.start()
