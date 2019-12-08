.. _ctxvals:

Context values
==============

SPyTEx provides support for "evaluation-contextual values" or *context values*
in short, which act like variables in a Python script.

Like variables, each context value exists within a specific scope. Context
values are often introduced by specific SPyTEx ``{...}`` constructs, such
values are generally only available *inside* the construct which creates them,
while they are undefined when evaluating constructs outside of it.

There are different ways to introduce context values in the evaluation, some of
them are explained here.


Referencing context values
--------------------------

Independently from how it is defined, a context value can be referenced in a
SPyTEx task with the ``{"=": "name"}`` construct. For example, the following
evaluates to the square of the context value bound to the ``foo`` name::

   {
     "!": "pow",
     "*": [{"=": "foo"}, 2]
   }

If no ``foo`` value is present in the current evaluation context, a
``KeyError`` is raised: this is what happens if you launch the ``spytex``
command providing the file above as input with no particular option.


Passing context values from command line
----------------------------------------

Context values can be set from the ``spytex`` command using the ``-c`` option.
The scope of such values is the whole expression contained in the input file,
thus they can be referenced anywhere, unless overwritten by other SPyTEx
constructs.

The basic format of the ``-c`` option is ``-c name=value``. For example, let's
run the file above (say it's named ``square.json``) setting 10 as the context
value assigned to the name ``foo``::

   $ spytex -c foo=10 square.json
   100

The ``-c`` option can be used multiple times to define multiple context
values::

   $ spytex -c foo=42 -c hello=world -c pi=3.14 task.json

Determining the value type
^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, the runtime type of a context value defined through the ``-c``
option can be ``int``, ``float`` or ``str`` and is automatically infered. The
following rules are applied to interpret a string ``X`` passed as value:

* if ``int(X)`` does not raise ``ValueError`` and ``str(int(X)) == X``, then
  return ``int(X)``
* else if ``float(X)`` does not raise ``ValueError``, then return ``float(X)``
* otherwise, return ``X`` as a string

If you need to overcome these rules or to get a value of a different type, you
can use the ``-c`` option with the ``-c name:type=value`` format, where
``type`` is the full dotted name of a function to which ``value`` is passed as
a string to get the actual value.

For example, to assign to ``foo`` the string ``"42"`` instead of the integer
``42``, you can launch::

   $ spytex -c foo:str=42 task.json

You can even pass more complex objects such as a complex number or a compiled
regular expression (quotes ``'...'`` are needed in bash and other shells to
avoid other interpretations of characters like ``\``)::

   $ spytex -c foo:complex=2+2i -c 'regex:re.compile=\d{4}-\d{2}-\d{2}'


Binding values to context
-------------------------

Another way to define context values is to insert into any SPyTEx ``{...}``
construct a ``=`` entry whose value is a mapping of one or more names to
values. Such values will be defined in the evaluation of *that* construct,
including other constructs nested in it but excluding any other construct
outside of it, even if SPyTEx evaluates it after the one with the ``=`` entry.
This functionality allows to define a value and have it evaluated by SPyTEx
only once and reuse it multiple times.

The following is an example of a context value computed once by calling the
``abs`` function and used twice to call the ``pow`` function::

   {
     "=": {
       "foo": {"!abs": -3}
     },
     "!": "pow",
     "*": [{"=": "foo"}, {"=": "foo"}]
   }

The equivalent Python script would be::

   foo = abs(-3)
   print(pow(foo, foo))
