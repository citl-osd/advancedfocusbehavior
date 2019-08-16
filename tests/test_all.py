import pytest

from importlib.util import find_spec
import subprocess
import sys

# Get list of tests
result = subprocess.run(['pytest', '--collect-only', '--ignore=tests/test_all.py', '-q', '--disable-warnings'],
                        stdout=subprocess.PIPE, text=True)

if result.returncode != 0:
    print(result.stdout)
    sys.exit(result.returncode)

tests = result.stdout.split('\n')[:-3]

use_coverage = bool(find_spec('pytest-cov'))


@pytest.mark.parametrize('test', tests)
def test_all(test):
    if use_coverage:
        cmd = ['pytest', '--cov-append', '--cov=kivy_garden/advancedfocusbehavior', test]

    else:
        cmd = ['pytest', test]

    test_results = subprocess.run(cmd)
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
