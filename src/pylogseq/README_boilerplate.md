**WARNING!** This Cookie should be used inside the **src** folder of a base **python** cookie. Do not use it standalone.

This is an example on how to configure a Python PyPI package for publishing.

The name of the parent folder must match the name of the package, as well as the main folder inside src. Inside that folder the package can be organized in submodules.


# Access PyDoc Documentation

Navigate to the package or **tests** folder and run **python -m pydoc -b**. Do this in the VSC terminal. A browser should open with the documentation.


# Testing the Package

To run tests, use **PyTest** and **PyTest-Watch** to watch/run.

Run tests at the **pytest.ini** level with **pytest-watch**. Configure PyTest running options at pytest.ini.

Since tests are run at package level, tests see the **tests/assets** folder as follows:

```python
# Read config file
with open("./tests/assets/Agenda/pages/A.md") as f:
    print("D: ", f.read())
```

Organize all tests in folders at **tests/src**. Do not create another tests folder at package level.

Test files must be named with the following structure: [a name]_test.py

Run them with **pytest -rP** to capture the **print** outputs.

Run a specific test:

```shell
# A specific test (a test class method)
pytest -rP -k "test_ping or test_apiinfo"

# A full module (a test class)
pytest -rP -k "TestClassWhatever"
```

**Pytest-Watch** can also be instructed to run only certain tests:

```shell
pytest-watch tests/parser_test.py tests/block_test.py
```


# Debugging inside VSC

To debug inside VSC, write **Pytest** tests and then use the **TESTING** panel. There selective runs of tests are possible in debug mode. The test will run and will stop at any breakpoint in code. All debugging infrastructure in VSC are then available.
