# Access PyDoc Documentation

Navigate to the package or **tests** folder and run **python -m pydoc -b**. Do this in the VSC terminal. A browser should open with the documentation.


# Testing the Package

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

    @pytest.mark.skip
    def test_b(self):
        """Another test.
        """
        assert 2 == 2
```


# Debugging inside VSC

To debug inside VSC, write **Pytest** tests and then use the **TESTING** panel. There selective runs of tests are possible in debug mode. The test will run and will stop at any breakpoint in code. All debugging infrastructure in VSC are then available.
