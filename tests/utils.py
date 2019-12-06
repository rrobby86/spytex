"""Test helpers"""


__all__ = "true", "false", "null", "task", "taskfile"


import os
import json

import pytest

from spytex import run
from spytex.compile import compile
from spytex.context import ResolutionContext


# JSON aliases for Python literals
true = True
false = False
null = None


_empty_context = ResolutionContext()


def _file(*path):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *path)


class TestTaskDescription:

    def __init__(self, descr):
        self.descr = descr

    def equals(self, expected, context=_empty_context):
        def testfun():
            task = compile(self.descr)
            assert task.resolve(context) == expected
        return testfun

    def raises(self, exception_type, context=_empty_context):
        def testfun():
            task = compile(self.descr)
            with pytest.raises(exception_type):
                task.resolve(context)
        return testfun


def task(descr):
    return TestTaskDescription(descr)


def taskfile(filename):
    with open(_file(filename), "r") as f:
        return TestTaskDescription(json.load(f))
