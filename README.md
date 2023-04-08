![AutoThalix](logo.png)

Repository that contains a toolkit to coduct complex operations on potentiostat.

Documentation: https://autothalix.readthedocs.io/en/latest/

## How to use

Usage of this package is demonstrated in [this repository](https://github.com/Arkady-A/AutoThalix_experiments). You can fork or clone it and start using it.

## Communication
### Report an issue or bug:

- Go to the repository's main page and click on the "Issues" tab.
- Click the "New Issue" button.
- Enter a descriptive title and a description of the issue.
- Add any relevant labels, milestones, or assignees.
- Click "Submit new issue."
 
### Request a new feature or enhancement:

- Go to the repository's main page and click on the "Issues" tab.
- Click the "New Issue" button.
- Enter a descriptive title and a detailed description of the feature or enhancement.
- Add the "enhancement" label.
- Add any relevant labels, milestones, or assignees.
- Click "Submit new issue."


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

