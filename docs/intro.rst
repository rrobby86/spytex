.. _intro:

Introduction
============

What SPyTEx does
----------------

The ``spytex`` command and the ``spytex.run`` function take as input a JSON
file with a specific syntax, interpret it and run Python code according to its
contents.

Why
---

Working on a ML project heavily customized and tuned around the application
domain, we found ourselves having to repeatedly test and push into production
new parameters for a task and sometimes even to change the task itself to be
executed, although reusing each time much of the existing code. This often
entailed the creation of new entry points in the codebase, in form of scripts
or CLI (sub)commands, each with its own well-defined set of options. We were
searching for a solution to define arbitrarily complex configurations for our
task with even the possibility to easily switch the task to be executed,
without having to define an ad-hoc CLI each time.

SPyTEx was created with the idea to have a global entry point in our codebase,
taking as input a JSON file which looks like an ordinary configuration file
with values for some parameters, but also allows to indicate an ordinary
function inside your code to be executed and to pass arbitrarily nested objects
as arguments. Whenever we want to test a new type of task accepting arbitrary
parameters, we can simply define an ordinary Python function in our codebase
and have it launched by SPyTEx; in simpler cases we may even define the whole
task by composing existing functions and classes into a SPyTEx JSON file.

SPyTEx JSON files somehow represent an alternative to custom Python scripts:
examples of JSON files throughout the docs will usually be accompanied with
their equivalent Python scripts. While being less intuitive at first, the use
of simple JSON allows the "script" to look more like a configuration file with
clear settable parameters and to be more easily handled by external tools, e.g.
stored in a `NoSQL database <https://en.wikipedia.org/wiki/NoSQL>`_ or
processed by `jq <https://stedolan.github.io/jq/>`_ or JSON APIs in any
language. Also, SPyTEx provides handy shortcuts for some operations, such as
calling other SPyTEx tasks or deserializing "pickled" objects from local or
remote files.

Main features
-------------

* Refer to arbitrary Python functions, classes and constants using their "full
  dotted name", e.g. ``json.load`` or ``urllib.request.urlretrieve``
* Arbitrarily compose existing functions and classes, e.g. calling a function
  or class constructor to obtain the argument to be passed to another function
* Easily refer to remote files (HTTP, SFTP, S3, ...) through integration of the
  `smart-open <https://pypi.org/project/smart-open/>`_ library

Security warning
----------------

Similarly to what the Python interpreter does when running a script, SPyTEx may
execute arbitrary Python code. It can be relatively easy to forge JSON files
with unwanted effects such as exposing secret information or deleting important
files. Only run SPyTEx on JSON files authored by you (or someone you trust),
**never run any file without knowing what it does!**
