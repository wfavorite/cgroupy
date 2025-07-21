# About this effort

## Why?

I wanted to brush up on a couple of things, so i wrote a Python class / module
to feed two hungry birds with one seed.

## Discovery time

This is a *list* of "Python things" that were interesting, frustrating, new, or just general notes i wanted to take.

> NOTE
>> My current "native tongue" is Go, so this is where one may expect comparisons between the languages. I try to admit biases when i *know* they are present: __Don't drag one language's idioms into another!__

## Packaging

One 'next step' for this project would be about making it a distributable *tool*. Something like [cx_Freeze](https://cx-freeze.readthedocs.io/en/stable/) would be a goto solution.

Old school Unix developers have been taught to avoid static binaries to save memory. (Yes, I am taking the *long* route to a point.) Statically compiled was *bad*. This made more sense than statically compiling in ``libc`` functions that were sure to be memory resident at any time on a memory constrained Unix system. These concerns have long ago taken a back seat to issues prevalent in modern development.

With the advent of "shopping cart" development where public libraries are brought in to solve all kinds of problems, it now becomes imperative to have deterministic behaviour of imported code. There are solutions for this, but the best solution (IMHO) for this is to force the issue at build time instead of run time.

> On: "shopping cart" development
>> This seems like a strongly biased term, but I am certainly not opposed to the concept. That said, "shopping" is an apt comparison as shoppers should be *informed* about what they are purchasing. Blindly importing a module/package may introduce a deeply flawed implementation or worse a security threat. This is not a Python-specific problem, but a relies-on-external-code problem.

For Rust and Go users, this is implicit in the development process. Python requires extra steps that came *after* the language grew in popularity.

I must admit that I would much prefer Rust or Go to binding this project into a single distributable object. The unhappy middle would probably be binding this into a single ``.py`` file which would be possible because it does not rely on modules outside the standard library. That would / should require *some* test coverage to guard against behaviour drift in the interpreter / standard libraries.

## Typing

Python variables are not (naturally) typed. I leveraged the "typing" module to handle this. (Despite it being in the standard library) I consider it a design 'bolt-on' / afterthought and not a first class capability in the language. The ability to create custom types as a first-class capability of the language in Go is a major win in comparison - IMHO.

Custom types in Go are really convenient for making "Lego pieces" that fit together in a more structured / rules-based manner. For example: in the CGroup class there is a concept of a *name* and a *path*. They are both strings representing directories, but one is a modified version of the other. Creating these as custom types would protect against accidentally mixing them.

The issue not properly handled here is the *grey area* between top-level structured data contracts and types. The sub-structures must be free-form lists/dicts as the internal/source data may vary by source system/version. User types for the different data structures in Go would probably be a nice fit here. (Perhaps this is some Go *bias* showing on my part.)

## Module / class structure

While not being a pure-OO type of person, I do respect the concepts when appropriate.

Here in the CGroup class there are static (file reader) methods that really belong to this class. They don't have any practical use outside the class; so I want them encapsulated *in* the class.

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

In fairness to Python and Java... the constraint is not without purpose or intent. If you are feeling uncomfortable about the size of a single file, it may be time to refactor.

## ``switch``

My *original* native tongue is C, and I have worked in just about all the C-ish/patterned languages (C++,Java,C#,Go) - so I *expect* a ``switch`` statement. I used the ``match`` statement which forces this project to require uplevel (>= 3.10) Python. This is only in the ``cgtool`` "test caller". I disabled it in favor of the more traditional if-elif-else as the Python version (on my Mac) was 3.9.6.

## Testing

> From the root of the project, run:
> ``python3 -m unittest``

There is minimal test coverage. While I am a steadfast fan of TDD, this is more about *discovery* than working towards an intended design. If I were intending to build a *specific* thing, then TDD would be far more appropriate & and easier.

''unittest'' appears to be a 'built-in' while there are lots of other test frameworks not explored here. The ``cgtool`` is a *rudimentary* stab at integration testing and should not be considered a proper solution.

Contrasting with Go...

Go also has similar built-in unit test capability. I think my bias (for Go unit tests) is probably rooted in recent familiarity with them. Generally in Go projects I have unit-tests integrated with the codebase (a standard pattern), but callable (via Make) in a project test directory with the integration testing (also a sort-of standard pattern).

> A clarification on the previous...
> Running ``make`` in a Go project would typically:
>
> - Build the binary (Does it build?)
> - Run unit tests (Does ``go test`` pass?)
> - Run integration tests (Does the binary/tool perform as expected?)

## Versions

I wrote this uplevel Python 3 - because I finally *can*. I have suffered from the "Python pinch" in large production environments where there are a smattering of "deep legacy" systems still running only Python 2 while the newly provisioned systems only have Python 3.

Writing code that can run in either was such a pain that I ported all Python code to Go - and never really looked back.

Here is to a world where that will never happen again.

## cgtool

This is just a wrapper for a PoC - not a proper tool. It either dumps a JSON structure of parsed data or a list of ingest errors.

Run the tool (against a real system) using:

``python3 cgtool``

Run the tool against local test data using:

``python3 cgtool -t``
