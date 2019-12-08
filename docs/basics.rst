.. _basics:

Basics
======

A SPyTEx input file is in practice an arbitrarily complex **Python expression**
which returns a value, **expressed in JSON**. The ``spytex`` command simply
parses, validates and evaluates the expression.


Literal values
--------------

Numbers, strings and literal values ``true``, ``false`` and ``null`` are
always evaluated to their Python equivalents, using the standard `json
<https://docs.python.org/3/library/json.html>`_ module. For example, the
following is a valid SPyTEx input file::

   42

Say this file is saved as ``foo.json``, you can "execute" it using the
``spytex`` command::

   $ spytex foo.json
   42

The command evaluates the expression and prints its result to standard output.

Other than simple literals, you can also obtain ``list`` and ``dict`` objects
using JSON arrays (``[...]``) and objects (``{...}``)::

   $ cat foo.json
   {
     "hello": "world",
     "foo": 42
   }

   $ spytex foo.json
   {'hello': 'world', 'foo': 42}

The object in the example above is interpreted by SPyTEx as a plain Python
``dict``, because keys (``hello`` and ``foo``) are generic strings. All the
rest of SPyTEx functionality is accessed using **objects with special keys**,
as seen in examples below and in the following sections.


Referencing Python objects
--------------------------

One basic requirement is to be able to reference Python objects defined either
in own codebase, in Python's standard library or in an external library.
Objects are referenced in SPyTEx using their *full dotted name*, having the
form ``package.subpackage.module.name``. For example, the ``pi`` constant
defined in Python ``math`` module can be referenced as ``math.pi``.

A reference to a Python object is expressed in SPyTEx as a JSON object with one
entry, whose key is ``.`` and whose value is the full dotted name of the
object. For example, by running ``spytex`` on the following file ::

   {".": "math.pi"}

we obtain the value of the referenced ``pi`` constant in the ``math`` module::

   3.141592653589793

Note that Python `builtin functions
<https://docs.python.org/3/library/functions.html>`_ and constants like
``True``, ``range``, ``abs``, ... can be referenced directly by their name. ::

   {".": "True"}

This references Python ``True`` constant, giving the same result as writing
``true`` directly in JSON.


Calling functions
-----------------

Other than retrieving objects defined in code, is important to be able to
*call* these objects. We usually need to call either functions to invoke them
or classes to obtain instances of them.

SPyTEx allows to call an object using the ``{"!": ...}`` notation, passing a
reference to the object to be called. For example, in order to call the
``random`` function of module ``random``, which returns a random number between
0 and 1, we can write the following file::

   {"!": {".": "random.random"}}

The result of invoking ``spytex`` on it will be a random number like this::

   0.4413500881143131

Given that objects to be called are usually obtained by a dotted name
reference, the ``!`` operator also accepts the name itself, so the example
above can be rewritten as::

   {"!": "random.random"}

Running this SPyTEx file is in practice equivalent to run this Python script::

   from random import random
   print(random())

Passing arguments
^^^^^^^^^^^^^^^^^

When calling functions (or other callables) we generally pass arguments to
them. In Python we can pass an arbitrary mix of *positional* and *keyword*
arguments.

To pass keyword arguments to a function call, you simply specify them as
additional key-value entries in the object containing the ``!`` key. For
example, the ``random.randint`` returns a random integer and accepts as
arguments ``a`` (the lower bound) and ``b`` (the upper bound); in order to call
it setting ``a`` to 1 and ``b`` to 6 (like rolling a die), we write::

   {
     "!": "random.randint",
     "a": 1,
     "b": 6
   }

The equivalent Python script would be::

   from random import randint
   print(randint(a=1, b=6))

To pass positional arguments, we use an additional entry in the call object
whose key is ``*`` and whose value is an array with the values. For example, to
call ``randint`` as above using positional arguments in place of keyword ones::

   {
     "!": "random.randint",
     "*": [1, 6]
   }

You can also pass both positional and keyword arguments. In the example below
we use ``random.choices`` to extract 2 random elements from given list (note
that ``*`` is a list with one argument, which is a list itself)::

   {
     "!": "random.choices",
     "*": [[4, 8, 15, 16, 23, 42]],
     "k": 2
   }

The equivalent Python script would be::

   from random import choices
   print(choices([4, 8, 15, 16, 23, 42], k=2))

Nested calls
^^^^^^^^^^^^

Positional and keyword arguments can be obtained by calling other functions,
obtaining an arbitrarily complex configuration of nested calls::

   {
     "!": "random.randint",
     "a": 1,
     "b": {
       "!": "pow",
       "*": [2, 4]
     }
   }

The equivalent Python script would be::

   from random import randint
   print(randint(a=1, b=pow(2, 4)))

Even the function to be called can be obtained by calling another function::

   {
     "!": {
       "!": "functools.partial",
       "*": [{".": "pow"}, 2]
     },
     "*": [4]
   }

The equivalent Python script would be::

   from functools import partial
   print(partial(pow, 2)(4))

1-posarg short syntax
^^^^^^^^^^^^^^^^^^^^^

In case you call a name-referenced function with exactly one positional
argument and no keyword ones, you can use the short syntax
``{"!dotted.name": "argument"}`` as long as the given name doesn't clash with a
magic function name. For example this ::

   {
     "!": "random.randrange",
     "*": [10]
   }

can be shortened into this ::

   {"!random.randrange": 10}
