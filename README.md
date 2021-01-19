## Installation

Step into desired folder and create new virtual environment:
```bash
python -m pip install --user virtualenv
```
```bash
python -m venv env
```
Activate virtual environment:

Windows:
```bash
.\env\Scripts\activate
```
Linux:
```bash
source env/bin/activate
```
Install required packages:
```bash
pip install -r requirements.txt
```
Download chromedriver from https://chromedriver.chromium.org/downloads

Place chromedriver.exe inside a folder. For example: 'C:\webdrivers'

Add path (C:\webdrivers) to system environment variables.

Modify parameters.py and fill secrets.py with credentials. Password must be a Gmail app password.

## Execution
Step into installation folder and activate virtual environment:

Windows:
```bash
.\env\Scripts\activate
```
Linux:
```bash
source env/bin/activate
```
Run:
```bash
python webscraper.py
```