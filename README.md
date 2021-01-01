## Installation (Windows)

Step into desired folder and create new virtual environment:
```bash
python -m pip install --user virtualenv
```
```bash
python -m venv env
```
Activate virtual environment:
```bash
.\env\Scripts\activate
```
Install required packages:
```bash
pip install -r requirements.txt
```
Modify parameters.py and fill secrets.py with credentials. Password must be a Gmail app password.

## Execution (Windows)
Step into installation folder and activate virtual environment:
```bash
.\env\Scripts\activate
```
Run:
```bash
python Webscraper.py
```