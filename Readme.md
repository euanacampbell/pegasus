<a href="url"><img src="/static/img/pegasus_icon.png" align="left" height="48" width="48" ></a>
<br>
# Pegasus

A command line tool for automating various tasks.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Pegasus.

```bash
pip3 install -r requirements.txt
```

## Usage

#### Web
Run the pegasus_web.py file, this will start a flask server and allow you to access it through the displayed location (http://127.0.0.1:5000/) in a browser.

```bash
python3 pegasus_web.py
```


#### Terminal
Run the pegasus_terminal.py file, this will load up the terminal version of Pegasus.

```bash
python3 pegasus_terminal.py

command: 
```

#### SQL
Use Pegasus to save and run queries more easily. Either navigate to /sqlsetup if using the web version, or manually modify the /configs/sql/yaml file.

Create connections to your commonly used databases for MySQL, SQL Server and Azure DBs. Save your queries, then group them together with a command. Include parameters in your queries with %p.

## Default Commands

- help (loads list of all available commands
- format (format json, sql, xml, and sql lists from your clipboard)
- sql (save and run your common sql queries)
- update (check and update to the latest version of Pegasus)

## Adding modules

Follow the below structure for any new modules.
Save this into the modules folder and import this at the top of the `main.py` file with the format `from modules.file_name import class_name`

```python
class command_name:
    """command description"""

    def __init__(self):
        self.config=config

    def __run__(self, param=None):
        """your code here"""
```


