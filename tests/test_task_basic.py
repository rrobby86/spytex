from datetime import date
from math import pi

from utils import *


# basic calls

test_pow = taskfile("pow.json").equals(9)

test_date_kw = task(
{
  "!": "datetime.date",
  "year": 2019,
  "month": 11,
  "day": 29
}
).equals(date(2019, 11, 29))

test_date_pos = task(
{
  "!": "datetime.date",
  "*": [2019, 11, 29]
}
).equals(date(2019, 11, 29))

test_pow_nested = task(
{
  "!": "pow",
  "*": [{
    "!": "pow",
    "*": [3, 2]
  }, 2]
}
).equals(81)

test_list_noarg = task(
{"!": "list"}
).equals([])

test_range_short = task(
{"!range": 4}
).equals(range(4))

test_ref_pi = task(
{".": "math.pi"}
).equals(pi)


# bindings
test_pow_bind = task(
{
  "=": {
    "foo": 3
  },
  "!": "pow",
  "*": [{"=": "foo"}, 2]
}
).equals(9)

test_pow_unbound = taskfile("pow_unbound.json").raises(KeyError)

test_pow_bind_run = task(
{
  "=": {
    "foo": 3
  },
  "!": "pow",
  "*": [{"!run": "pow_unbound.json"}, 2]
}
).equals(81)
