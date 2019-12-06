from utils import *


test_pow_run = task(
{
    "!": "pow",
    "*": [{"!run": "pow.json"}, 2]
}
).equals(81)

test_pow_unpickle = task(
{
    "!": "pow",
    "*": [{"!unpickle": "9.pickle.bin"}, 2]
}
).equals(81)

test_env_foo = task(
{"!env": "SPYTEX_TEST_FOO"}
).equals("foo")
