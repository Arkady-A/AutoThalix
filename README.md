![AutoThalix](logo.png)

Repository that contains a toolkit to coduct complex operations on potentiostat.

## How to use

Usage of this package is demonstrated in [this repository](https://github.com/Arkady-A/AutoThalix_experiments). You can fork or clone it and start using it.


## Participate in development

Run this command to create virtual environment:

````
python -m venv venv
````

Run this command to activate virtual environment:

````
source venv/bin/activate
````

### Install requirements

Run this command in virtual environment to install all dependencies:

````
pip install -r requirements.txt
````

### Run tests

Run this command in virtual environment to install all dependencies for tests:

````
pip install -r requirements-test.txt
````

Run this command to run all tests:

````
pytest
````

Run this command to run all tests with coverage and open coverage report in browser:

````
pytest --cov=thales --cov-report=html && open htmlcov/index.html
````

