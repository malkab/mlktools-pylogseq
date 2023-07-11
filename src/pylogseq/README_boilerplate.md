# Building the Wheel Package

Run the **010** script to build the package and install it with PIP. This will make it available to any companion CLI program, for example.

The Wheel package **.whl** will be stored at **dist** folder.


# Access PyDoc Documentation

Navigate to the package folder and run **python3 -m pydoc -b**. Do this in the VSC terminal. A browser should open with the documentation.


# Testing the Package

**NOTICE:** run always the package folder, right above the **tests** and the package folder, and configure paths to assets accordingly. If not, the watching will not affect the source files.

Tests access the package assets directly this way:

```python
from package import Something

# TESTS HERE
```

To run tests:

```shell
# Run with watch at pytest.ini level, all tests
pytest-watch

# Run with warch certain tests
pytest-watch tests/parser_test.py tests/block_test.py

# A specific test (a test class method), capturing prints
pytest -rP -vvv -k "test_ping or test_apiinfo"

# A full module (a test class), capturing prints
pytest -rP -vvv -k "TestClassWhatever"
```

To run tests, use **PyTest** and **PyTest-Watch** to watch/run.

Run tests at the **pytest.ini** level with **pytest-watch**. Configure PyTest running options at pytest.ini.

Since tests are run at package level, tests see the **tests/assets** folder as follows:

```python
# Read config file
with open("./tests/assets/Agenda/pages/A.md") as f:
    print("D: ", f.read())
```

Organize all tests in folders at **tests**. Do not create another tests folder at package level.

Test files must be named with the following structure: [a name]_test.py


# Skipping Tests

To skip a test, use the decorator:

```python
@pytest.mark.skip
class TestA:
    """_summary_
    """

    def test_b(self):
        """Another test.
        """
        assert 2 == 2
```


# Debugging inside VSC

To debug inside VSC, write **Pytest** tests and then use the **TESTING** panel. There selective runs of tests are possible in debug mode. The test will run and will stop at any breakpoint in code. All debugging infrastructure in VSC are then available.
