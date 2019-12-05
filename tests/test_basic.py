from datetime import date
from math import pi

from utils import task_returns, task_raises


# basic calls
test_pow = task_returns("pow.json", 9)
test_date_kw = task_returns("date_kw.json", date(2019, 11, 29))
test_date_pos = task_returns("date_pos.json", date(2019, 11, 29))
test_pow_nested = task_returns("pow_nested.json", 81)
test_list_noarg = task_returns("list_noarg.json", [])
test_range_short = task_returns("range_short.json", range(4))
test_ref_pi = task_returns("pi.json", pi)

# bindings
test_pow_bind = task_returns("pow_bind.json", 9)
test_pow_unbound = task_raises("pow_unbound.json", KeyError)
test_pow_bind_run = task_returns("pow_bind_run.json", 81)

# magics
test_pow_run = task_returns("pow_run.json", 81)
test_pow_unpickle = task_returns("pow_unpickle.json", 81)
test_env_foo = task_returns("env_foo.json", "foo")

# sequential
test_seq_one = task_returns("seq_one.json", 9)
test_seq_two = task_returns("seq_two.json", 16)
test_seq_two_var = task_returns("seq_two_var.json", 81)
