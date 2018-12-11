# pythonic_integer

Implement a class that has all of the features and characteristics
of the mathematical object "integer", without importing _any_ module.

## Testing
To start, you'll need [pipenv](https://docs.pipenv.org/) from either
Homebrew or `pip`. Then, clone the repo and from the repo root, run 
```bash
pipenv install --dev
```
This will install the packages specified in Pipfile into a virtual
environment, and activate that virtual environment. Then, to run
the test suite, execute the following:
```bash
pipenv run python -m pytest -v test/
```
