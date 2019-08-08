import pytest

import subprocess
import sys

# Get list of tests
result = subprocess.run(['pytest', '--collect-only', '--ignore=tests/test_all.py', '-q', '--disable-warnings'],
                        stdout=subprocess.PIPE, text=True, check=True)

tests = result.stdout.split('\n')[:-3]
#print(tests)


@pytest.mark.parametrize('test', tests)
def test_all(test):
    print(test)
    test_results = subprocess.run(['pytest', test])
    assert test_results.returncode == 0


# Run without pytest
if __name__ == '__main__':
    results = []
    for test in tests:
        try:
            test_all(test)
            passed = True

        except AssertionError:
            passed = False

        results.append(f'{"PASS" if passed else "FAIL"} - {test}')

    for res in results:
        print(res)
