# Potential extensions to this project

This is not intended (at this time) to be a comprehensive *cgroup tool*, but instead is about investigating concepts and ideas. This is a working list of what might be directions to follow.

## /proc integration

cgroups know about what processes they contain (``cgroup.procs``) and processes know about what cgroup they belong to (via ``/proc/self/cgroup``). Discovery and reporting of cgroups would be enhanced by tying more meaningful process information to them.

## Known invalid items

A number of conditions cause cgroup configurations to be invalid such as:

- Dangling (/deleted) cgroup references in zombie processes
- Hierarchial definitions that are invalid (such as configuration options not supported by the parent)

These could be included in the discovery process and flagged as part of analysis tools.

## Selective data gathering

It would be appropriate to tie data collection to required items. The two primary selectors would be:

- What is appropriate for the config. Not all cgroups have the same controllers, and therefore do not have the same "controls" / files. Such a tool should have awareness of what *should* exist as data sources.
- What is appropriate for the query. If a user requested information based on a single controller, then it would not be appropriate to (attempt to) collect information on all controllers.

The design of the ``cgroup2`` filesystem interface is keyed appropriately for this purpose.
