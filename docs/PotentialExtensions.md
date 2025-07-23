# Potential extensions to this project

This is not intended (at this time) to be a comprehensive *cgroup tool*, but instead is about investigating concepts and ideas. This is a working list of what might be directions to follow.

## /proc integration

cgroups know about what processes they contain (``cgroup.procs``) and processes know about what cgroup they belong to (via ``/proc/self/cgroup``). Discovery and reporting of cgroups would be enhanced by tying more meaningful process information to them.

## Known invalid items

A number of conditions cause cgroup configurations to be invalid such as:

- Dangling (/deleted) cgroup references in zombie processes
- Hierarchial definitions that are invalid (such as configuration options not supported by the parent)

These could be included in the discovery process and flagged as part of analysis tools.

Rules could be applied - much like "linter rules" to a config. Such a ruleset may be more appropriate to performing 'actions' such as modifying a cgroup or adding PIDs as discussed in "Discovery / actions" below.

## Selective data gathering

It would be appropriate to tie data collection to required items. The two primary selectors would be:

- What is appropriate for the config. Not all cgroups have the same controllers, and therefore do not have the same "controls" / files. Such a tool should have awareness of what *should* exist as data sources.
- What is appropriate for the query. If a user requested information based on a single controller, then it would not be appropriate to (attempt to) collect information on all controllers.

The design of the ``cgroup2`` filesystem interface is keyed appropriately for this purpose.

## Discovery / actions

> This is an extension to the "Known invalid items" above.

Rules for taking actions (like modifying controllers, PIDs, threads...) are based on the current config. Like PIDs cannot be added to non-leaf or 'dying' cgroups, resources not belonging to the parent cannot be managed in the client, controllers cannot be modified until they are made active in the subtree_control file... If a tool were to be created that managed cgroups (or *a* specific cgroup), then this discovery would be helpful in preventing invalid configuration actions.

Potential actions:

- Adding / moving PIDs between cgroups
- Delegating access
- Managing resources
- Feature mapping from ``/sys/kernel/cgroup`` files
