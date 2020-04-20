# smart-pharmacy-fridge

This repo holds the implementation of the Smart Pharmacy Fridge system.

Requirements:
- Python 3.6+

To start, create a virtual environment:
`python -m venv venv`

Then, activate the virtual environment:
`source venv/bin/activate`

On Windows:
`venv\Scripts\activate`

Install Python dependencies:
`pip install -r requirements.txt`

Start app:
`flask run`

Leave virtual environment:
`deactivate`

The db.db file can be explored with a DB explorer such as: <https://sqlitebrowser.org/>

Testing:
`coverage run test_run.py`

Test coverage report:
`coverage report`