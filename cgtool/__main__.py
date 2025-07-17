
# ^
# |
# +- No magic here. Not intended for production use!

import json
import sys

from CGroup import CGroup

# ============================================================================
def main():

    # IMPORTANT NOTE:
    # This is NOT a production tool! It is just a calling 'framework' for the
    # class. If a *single* argument is detected, it is taken to be the
    # alternate data source (or a flag to test).

    use_src =""

    # Using the uplevel nested 'switch' pattern.
    #match len(sys.argv):
    #    case 1:
    #        # No-op
    #        pass
    #    case 2:
    #        match sys.argv[1]:
    #            case "-t":
    #                use_src = 'data/sys/fs/cgroup'
    #            case _:
    #                use_src = sys.argv[1]
    #    case _:
    #        sys.stderr.write("ERROR: Unknown number of arguments")
    #        sys.exit(1)

    # The more idiomatic pattern - admittedly not that ugly (despite my 
    # biases).
    argv_len = len(sys.argv)
    if argv_len == 2:
        if sys.argv[1] == "-t":
            use_src = 'data/sys/fs/cgroup'
        else:
            use_src = sys.argv[1]
    elif argv_len > 2:
        sys.stderr.write("ERROR: Unknown number of arguments")
        sys.exit(1)

    # I *prefer* to have a clear declaration of a variable in cases like this.
    # Python does not require it - that may make it look strange.
    cg = None
    if not use_src:
        cg = CGroup()
    else:
        cg = CGroup(use_src)

    # Pedantic assertions are my specialty.
    if not cg:
        sys.stderr.write("ASSERT: Reached what should be the unreachable.")

    # This is not a requirement. The class uses 'RAII' so it ingests on
    # initialization.
    # cg.Ingest()

    errors = cg.IngestErrors()
    if len(errors) > 0:
        for error in errors:
            sys.stderr.write(f'{error}\n')
        sys.exit(1)


    cgroups = cg.CGroups()


    jdata = json.dumps(cgroups, indent=2)
    sys.stdout.write(jdata)
    sys.stdout.write("\n")

# ============================================================================
# I did this... it might have been more appropriate / simpler to just include
# it in the class.
if __name__ == "__main__":
    main()