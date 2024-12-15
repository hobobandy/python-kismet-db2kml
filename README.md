# python-kismet-db2kml
Python GUI to generate KML files of device locations from KismetDB files.

## Better Alternative?
Kismet nowadays provides its own KML generation script with more features than this script. [Read more here](https://www.kismetwireless.net/docs/readme/kismetdb/kismetdb_kml/)

## Installation

### Python Version

* Python 3.13

### Python Packages

- Colour
- SimpleKML
- Peewee

### Using pip

1) Recommendation: Create a new virtual environment using `python -m venv .venv` inside the project's folder. Activate using your platform's script under `.venv/Scripts/` (e.g. activate.bat for Windows, activate for Linux).

2) Install required packages: `pip install -r requirements.txt`

## Background
This was part of small projects to learn how to develop Tk GUIs on Windows.

If needed to run in a single exe, it can easily be packaged with [PyInstaller](https://pyinstaller.org/en/stable/).
