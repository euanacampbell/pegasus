# Pegasus

A command line tool for automating various tasks.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Pegasus.

```bash
pip3 install -r requirements.txt
```

## Usage

Run the main.py file, this will load up the prompt.

```bash
python3 main.py

command: 
```

## Default Commands

- help (loads list of all available commands
- jsonformat (formats a json model in your clipboard)
- sqlformat (formats a SQL command in your clipboard)
- listformat (formats a list into a SQL queryable list)

## Adding modules

Follow the below structure for any new modules.
Save this into the modules folder and import this at the top of the `main.py` file with the format `from modules.file_name import class_name`

```python
class command_name:
    """command description"""

    def __init__(self, config=None):
        self.config=config

    def __run__(self, param=None):
        """your code here"""
```


