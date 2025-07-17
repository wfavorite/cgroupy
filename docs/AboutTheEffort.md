# About this effort

## Why?

I wanted to brush up on a couple of things, so i wrote a Python class / module
to feed two birds with one seed.

## Discovery time

This is a *list* of "Python things" that were interesting, frustrating, new, or just general notes i wanted to take.

> NOTE
>> My current "native tongue is Go, so this is where one may expect comparisons.

## Typing

Variables are not (naturally) typed. I leveraged the "typing" module to handle this. I consider it a 'bolt-on' and not a first class capability in the language. The ability to create custom types as a first-class capability of the language in Go is a major win in comparison.

The issue not properly handled here is the *grey area* between top-level data contracts and types. The sub-structures must be lists/dicts as the internal data may vary. User types for the different data structures in Go would probably be a nice fit here. (Perhaps this is some Go *bias* showing on my part.)

## Module / class structure

While not being a pure-OO type of person, I do respect the concepts when appropriate.

Here in the CGroup class there are static (file reader) methods that really belong to this class. They don't have any practical use outside the class; so i want them *in*.

The *problem* is that breaking these (static) methods out is sort of an *anti-pattern* for Python. There are examples of how to do it (Basically you import *within* the class), but it is not nice. To be clear; it can be done - it is just not a *standard* pattern.

Java (colour me stoopid) forces the same constraint. A class definition must be in one file. I seem to recall that C# let me do it (although it was not a standard pattern).

Go allows me to do the following (all in directory sort-order beauty):

```text
MyClassType.go         <---- The data structure definition.
MyClassTypePublic.go   <---- Public methods.
MyClassTypePrivate.go  <---- Private methods.
MyClassType_test.go    <---- Unit tests.
```

I like this because it allows me to separate concerns within a 'class'.

In fairness to Python and Java... the constraint is not without purpose. If you are feeling uncomfortable about the size of a single file, it may be time to refactor.

## ``switch``

My *true* native tongue is C, and i have worked in just about all the C-ish/patterned languages (C++,Java,C#,Go) - so i *expect* a ``switch`` statement. I used the ``match`` statement which forces this project to require uplevel (>= 3.10) Python. This is only in the ``cgtool`` "test caller". I disabled it as the python version (on my Mac) was 3.9.6.

## Testing

> From the root of the project, run:
> ``python3 -m unittest``

''unittest'' appears to be a 'built-in' while there are lots of other test frameworks not explored here.

Contrasting with Go...

Go also has similar built-in unit test capability. I think my bias (for Go unit tests) is probably rooted in familiarity. Generally in Go projects I have unit-tests integrated with the codebase (a standard pattern), but callable (via Make) in a project test directory with the integration testing (also a sort-of standard pattern).

## cgtool

This is just a wrapper for PoC - not a proper tool. It either dumps a JSON structure of parsed data or a list of ingest errors.

> Run the tool using:
> ``python3 cgtool``
