Place Python tests here.

Test files must be named with the following structure: [a name]_test.py

Run them with **pytest -rP** to capture the **print** outputs.

Run a specific test:

```shell
# A specific test (a test class method)
pytest -rP -k "test_ping or test_apiinfo"

# A full module (a test class)
pytest -rP -k "TestClassWhatever"
```
