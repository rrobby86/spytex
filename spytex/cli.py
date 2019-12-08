import sys
import re
import pickle
from argparse import ArgumentParser
from pydoc import locate

from smart_open import open

from . import __version__
from .api import run
from .context import ResolutionContext


_CTXVAL_PTN = re.compile(r"([A-Za-z0-9_]+)(?::([A-Za-z0-9_\.]+))?=(.*)")


def _autotyped_value(text):
    try:
        toint = int(text)
        if str(toint) == text:
            return toint
    except ValueError:
        pass
    try:
        tofloat = float(text)
        return tofloat
    except ValueError:
        pass
    return text


def _parse_ctxval_option(text):
    m = _CTXVAL_PTN.fullmatch(text)
    if not m:
        raise Exception("invalid context value specification: " + text)
    if m.group(2):
        converter = locate(m.group(2))
        value = converter(m.group(3))
    else:
        value = _autotyped_value(m.group(3))
    return m.group(1), value


def main():
    parser = ArgumentParser()
    parser.add_argument("task_file", nargs="?", metavar="TASK",
                        help="task specification file")
    parser.add_argument("-c", dest="vals", action="append",
                        metavar="KEY[:TYPE]=VAL", help="set context value")
    parser.add_argument("-p", "--pickle", metavar="FILE",
                        help="pickle returned object to specified file")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="suppress output of returned value")
    parser.add_argument("--version", action="version",
                        version="SPyTEx {}".format(__version__))
    args = parser.parse_args()
    context = ResolutionContext()
    if args.vals:
        values = dict(map(_parse_ctxval_option, args.vals))
        context = context.update_vals(values)
    result = run(args.task_file or sys.stdin, context)
    if result is not None and not args.quiet:
        print(result)
    if args.pickle:
        with open(args.pickle, "wb") as f:
            pickle.dump(result, f)
