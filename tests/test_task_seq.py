from utils import *


test_seq_one = task(
{
  "!sequential": [
    {
      "!": "pow",
      "*": [3, 2]
    }
  ]
}
).equals(9)

test_seq_two = task(
{
  "!sequential": [
    {
      "!": "pow",
      "*": [3, 2]
    },
    {
      "!": "pow",
      "*": [4, 2]
    }
  ]
}
).equals(16)

test_seq_two_var = task(
{
  "!sequential": [
    {
      ":=": "foo",
      "!": "pow",
      "*": [3, 2]
    },
    {
      "!": "pow",
      "*": [{"=": "foo"}, 2]
    }
  ]
}
).equals(81)
