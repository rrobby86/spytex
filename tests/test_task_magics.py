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

test_eval_basic = task(
{"!eval": "2+2"}
).equals(4)

test_eval_context = task(
{
    "=": {
        "N": 8
    },
    "!eval": "2**N - 1"
}
).equals(255)

test_eval_unbound = task(
{"!eval": "x+2"}
).raises(NameError)

test_env_foo = task(
{"!env": "SPYTEX_TEST_FOO"}
).equals("foo")
