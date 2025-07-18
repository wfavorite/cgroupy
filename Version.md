# Version documentation

## Version history

```text
0.1.0   16-7-25 - Initial creation.
0.2.0   17-7-25 - Cleaned up the class.
                - Implemented an error capturing method(ology).
                - Added a README as github desires.
0.3.0   18-7-25 - Added assertRaises() checks (with bad input) to unit test.
                - Not proper TDD, but adding additional testing forces design
                  issues to the surface. In this case the parsing rules around
                  expected file formats was tightened. Discussion can be found
                  in the CGroup class documentation.
                - All tests pass.
                - Added tests to cover unexpected / edge-cases and assertions.
                  Again... these drive *and* cover expected behaviours. This
                  includes setup and tear-down of testing conditions that git
                  will not support.
                  Some things done:
                  * Dumping more / structured data in the unittest assertions.
                    It is nice to have the bad data when it fails rather than
                    needing to go figure it out.
                  * Setup and tear down of test conditions around the tests.
                - All tests pass.

```

## Todos

```text
[ ] Research explicit decorators for public / private.
[_] Research additional testing.
[ ] Setup a github action for automated testing.
[ ] Design for how this might be distributed in / 'frozen' for a real
    deployment.
[Q] Create a custom exception type. (I am Questioning this. It may be more
    appropriate to just focus on internal assert()ions vs user-ish errors.)
[_] Clean up the module/class definition / design.
```

## Done

```text
[X] Add a top-level README.
[X] Into git.
[X] Resolve the error handling problem.
```
