# xonnel-test

A python library: xonnel-test

- configurable assert wrapper
    - onfail actions:
        - raise (default)
        - print

    - onpass actions:
        - raise
        - print (default)

    - works with any of:
        - callables (if returning a bool when eveluated)
        - booleans

## Install

LOCAL:
cd xonnel-test
pip install -e .

PyPI:
pip install xonnel-test
