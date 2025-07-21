# cgroupy

A (public) PoC / discovery project for the kind of tool development I might be called to create.

I wrote it to polish up on some skills. This is not for public use, unless the use is to read my work / style.

> __NOTE__
>> This is NOT a complete implementation - just kicking around some concepts. This is not to be used in a production environment or under production conditions.

## About

This is a (wrapper around a) class to read in cgroup configurations. Potential uses are for off-system QC or comparisons / deltas with other system configurations.

At this point it is just a day-ish of work, so is __far from complete__ with minimal test coverage.

## Quick links

### Documentation

- [The version file](Version.md) - Contains version and todos.
- [About The Effort](docs/AboutTheEffort.md) - Loose notes on things perhaps worth remembering or thinking about.
- [Potential next steps](docs/PotentialExtensions.md) - Potential non-PoC applications of this effort.

### Code

> __NOTE__
>> I use the STUB keyword of inline-todos and hanging issues. I also use whitespace to denote things unresolved. (If a chunk of code is surrounded by whitespace, it is for a reason.) I also use the VOIR keyword for "hey look at this" kind of 'findings'. Both light up like christmas trees in my editor.

- [The CGroup class](cgtool/CGroup/__init__.py)
- [The cgtool tester](cgtool/__main__.py)
- [Unit tests](tests/test_cgmod.py)
