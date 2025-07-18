
import os
from typing import List, Dict


# STUB: Document the class better.

class CGroup:
    """
    CGroup is a utility class for ingesting all cgroup definitions on a
    system. It may be used for detecting problems in a config or for comparison
    between systems.

    On the issue of invalid input
    The thinking is that the input is only well-formatted files. In the Linux
    world, these (specific) files are APIs. If an API is not behaving correctly
    then something bad and unexpected has happened. The correct approach is to
    throw an assertion when well defined interfaces change unexpectedly rather
    than to proceed and drop or misconstrue data.
    """

    

    DEFAULT_CGROUP_DIR = '/sys/fs/cgroup'
    cgdir = DEFAULT_CGROUP_DIR

    TOP_PARENT_NAME = "root"

    # ========================================================================
    def __init__(self, cgdir=None):
        
        # This value can be overridden for test.
        if cgdir is not None:
            self.cgdir = cgdir
    
        # Initialize these
        self.discovered_cgroups = []
        self.discovery_errors = ["Discovery not completed."]

        # RAII - What else are we called for?
        self.Ingest()
    
    # ========================================================================
    def Ingest(self):
        """
        Ingests all cgroup definitions. Discovery/ingestion is done at class
        initialization. This refreshes the discovery / discovery errors.

        Args:
            None

        Returns:
            None

        Raises:
            None: Use the IngestErrors method to see if errors were encountered.
        """

        # Initialize/reset the list.
        self.discovered_cgroups = []
        # Same for the error list
        self.discovery_errors = []
        
        # Kick off a recursive scan of the top cgroup directory.
        self.ingest_cgroup_dir(self.cgdir, self.TOP_PARENT_NAME)
        

    # ========================================================================
    def IngestErrors(self) -> List:
        """
        Returns a list of errors encountered during ingest.
        
        Args:
            None

        Returns:
            List: Potentially empty list of errors encountered during ingest.

        Raises:
            None

        """
        return self.discovery_errors


    # ========================================================================
    def CGroups(self) -> List:
        """
        Returns a list of ingested cgroups.

        Args:
            None

        Returns:
            List: Potentially empty list of cgroup definitions.

        Raises:
            None
        """
        return self.discovered_cgroups



    # ========================================================================
    def ingest_cgroup_dir(self, dir: str, parent: str):
        """
        Recursively scan the provided cgroup directory for sub-cgroup
        directories.
        
        Args:
            dir (string): The /sys/fs/cgroup directory.
            parent (string): The parent cgroup name of this directory/cgroup.
        """

        # Get this cgroup/directory
        try:
            name = CGroup.derive_name_from_path(dir)
            this_cgroup, failures = CGroup.ingest_cgroup(dir, name, parent)
            self.discovered_cgroups.append(this_cgroup)
            for failure in failures:
                self.discovery_errors.append(failure)
        except Exception as e:
            err_msg = f'Failed to ingest dir-cgroup: {repr(e)}'
            self.discovery_errors.append(err_msg)

        # Now look for all the children
        try:
            with os.scandir(dir) as cgroup_entries:
                for entry in cgroup_entries:
                    if entry.is_dir():
                        # Grab this 'child' entry
                        name = entry.name
                        child_dir = os.path.join(dir, name)
                        self.ingest_cgroup_dir(child_dir, this_cgroup['name'])                        
        except Exception as e:
            err_msg = f'Failed to scan {dir}: {repr(e)}'
            self.discovery_errors.append(err_msg)
            

    # ========================================================================
    @staticmethod
    def derive_name_from_path(dir: str) -> str:
        """
        Derives the cgroup name from the final directory-path entry.

        Args:
            dir (string): The /sys/fs/cgroup/ subdirectory.

        Returns:
            string: The last directory name.
        """

        # Exceptions may escape here, but they are effectively internal errors
        # or assertions.
        if not dir:
            raise ValueError

        parts = os.path.split(dir)

        if len(parts) != 2:
            raise ValueError

        return parts[1]



    # ========================================================================
    @staticmethod
    def ingest_cgroup(dir: str, name: str, parent: str) -> tuple[Dict, List]:
        """
        Ingests the cgroup (/sys file) configuration.
        
        Args:
            dir (string): The cgroup directory.
            name (string): The name of the cgroup.
            parent (string): The cgroup's parent name.

        Returns:
            Dict: A structured representation of the cgroup configuration.
            List: A list of errors encountered.
            
        """

        cgroup = {}
        errors = []

        cgroup['name'] = name
        cgroup['parent'] = parent

        # Now read in all the data. Exceptions are collected and converted
        # into error messages here.
        # When failed, create an empty version of the expected thing.
        try:
            filename = 'cgroup.controllers'
            proper_path = os.path.join(dir, filename)
            cgroup['cgroup_controllers'] = CGroup.ingest_controllers(proper_path)
        except Exception as e:
            err_msg = f'Failed to ingest {filename}: {repr(e)}'
            errors.append(err_msg)
            cgroup['cgroup_controllers'] = []
            
        try:
            filename = 'cgroup.stat'
            proper_path = os.path.join(dir, filename)
            cgroup['cgroup_stat'] = CGroup.ingest_stdkv(proper_path)
        except Exception as e:
            err_msg = f'Failed to ingest {filename}: {repr(e)}'
            errors.append(err_msg)
            cgroup['cgroup_stat'] = {}

        try:
            filename = 'cpu.stat'
            proper_path = os.path.join(dir, filename)
            cgroup['cpu_stat'] = CGroup.ingest_stdkv(proper_path)
        except Exception as e:
            err_msg = f'Failed to ingest {filename}: {repr(e)}'
            errors.append(err_msg)
            cgroup['cpu_stat'] = {}

        try:
            filename = 'cgroup.max.depth'
            proper_path = os.path.join(dir, filename)
            cgroup['cgroup_max_depth'] = CGroup.ingest_single_line_file(proper_path)
        except Exception as e:
            err_msg = f'Failed to ingest {filename}: {repr(e)}'
            errors.append(err_msg)
            cgroup['cgroup_max_depth'] = ""

        try:
            filename = 'cgroup.max.descendants'
            proper_path = os.path.join(dir, filename)
            cgroup['cgroup_max_descendants'] = CGroup.ingest_single_line_file(proper_path)
        except Exception as e:
            err_msg = f'Failed to ingest {filename}: {repr(e)}'
            errors.append(err_msg)
            cgroup['cgroup_max_descendants'] = ""

        return cgroup, errors



    # ========================================================================
    @staticmethod
    def ingest_controllers(fn: str) -> List:
        """
        Ingests the list of controllers from the cgroup.controllers file.

        Args:
            fn (str): The filename

        Returns:
            list: A list of controllers for that cgroup
        """

        controllers = []

        # No try, let exceptions escape.
        with open(fn) as controllers_file:
            # The (strict) expectation of this file is that it is a single
            # line. Treat it as such - at least for the simple parse case.
            #
            # Meaning:
            #  - readline() should protect us from EOLs or other nonsense
            #    in the file.
            #  - split() should never have the oppurtunity to split on any
            #    other type of whitespace.
            #
            # If read() is used instead of readline(), this may parse an
            # invalid file.
            first_line = controllers_file.readline()
            controllers = first_line.split()

            # This should be empty - throw if it is not.
            next_line = controllers_file.readline()
            if len(next_line) > 0:
                raise Exception("Single line file has multiple lines")


        return controllers

    # ========================================================================
    @staticmethod
    def ingest_stdkv(fn: str) -> Dict:
        """
        Ingests a standard key-value file common to cgroups.

        Args:
            fn (string): The filename to ingest

        Returns:
            dict: A dictionary of key value pairs.

        Raises:
            Any & all exceptions encountered.
        """

        kvpairs = {}

        # Do not 'try' - let exceptions escape.        
        with open(fn) as kvfile:
            for line in kvfile:
                pair = line.split()

                # One option might be to skip over this oddity, but since this
                # is a well formatted file provided by an 'API' i think the
                # assertion (blow it all up) is more appropriate.
                #
                # So, given the choice...
                #  1. Drop the offending line. Return a list of parse errors.
                #  2. Consider the file (or the parser) invalid, and fix.
                #
                # I chose option 2.
                if len(pair) != 2:
                    raise Exception("Invalid key-value line in key-value file")

                key = pair[0]
                value = pair[1]
                kvpairs[key] = int(value)

        return kvpairs

    # ========================================================================
    @staticmethod
    def ingest_single_line_file(fn: str) -> str:
        """
        Ingests a single value file common to cgroups.

        Args:
            fn (string): The filename to ingest.

        Returns:
            string: The entire contents of the file.

        Raises:
            Any & all exceptions encountered.
        """

        content = ""

        # Do not 'try' - let exceptions escape.        
        with open(fn) as simple_single:
            # This will chomp the line -----------+
            # This grabs only the first +         |
            #                           V         V
            content = simple_single.readline().rstrip()

        return content
