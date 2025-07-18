#!/usr/bin/python3

import unittest

import json
import os

from cgtool.CGroup import CGroup

# ============================================================================
class TestCGroup(unittest.TestCase):

    # ========================================================================
    # setUp preps the 'file system' for the test.
    def setUp(self):
        # This has to happen in the test because git can't save it otherwise.
        os.chmod("data/bad/fs/cgroup/cgroup.max.descendants", 0o333)
        
        return super().setUp()

    # ========================================================================
    # tearDown restores the 'file system' to proper state.
    def tearDown(self):
        # Set this back so git can manage it.
        os.chmod("data/bad/fs/cgroup/cgroup.max.descendants", 0o644)

        return super().tearDown()
    
    # ========================================================================
    # test_controllers covers the ingest_controllers() (static) method.
    def test_controllers(self):
      
        # Properly formatted file.
        controllers = CGroup.ingest_controllers("data/sys/fs/cgroup/cgroup.controllers")
        controllers_count = len(controllers)
        controllers_expected = 9
        self.assertEqual(controllers_count,controllers_expected, f'Expected {controllers_expected} controllers; got {controllers_count}')

        # File does not exist.
        with self.assertRaises(Exception):
            controllers = CGroup.ingest_controllers("data/bad/fs/cgroup/cgroup.controllers.not")

        # Spaces replaced with EOLs
        with self.assertRaises(Exception):
            controllers = CGroup.ingest_controllers("data/bad/fs/cgroup/cgroup.controllers.1")

    # ========================================================================
    # test_cgingest covers the ingest_cgroup() (static) method.
    def test_cgingest(self):

        # ----------
        # The good
        cgroup, errors = CGroup.ingest_cgroup("data/sys/fs/cgroup", "cgroup", "TOP")
        
        errors_count = len(errors)
        errors_expected = 0
        self.assertEqual(errors_count,errors_expected, f'Expected {errors_expected} errors; got {errors_count}')

        cgroup_controllers = cgroup['cgroup_controllers']
        controllers_count = len(cgroup_controllers)
        controllers_expected = 9
        self.assertEqual(controllers_count,controllers_expected, f'Expected {controllers_expected} controllers; got {controllers_count}')

        cgroup_stat = cgroup['cgroup_stat']
        stat_kv_count = len(cgroup_stat)
        stat_kv_expected = 22
        self.assertEqual(stat_kv_count,stat_kv_expected, f'Expected {stat_kv_expected} kv-pairs; got {stat_kv_count}')

        #nr_subsys_cpuset 93
        stat_kv_value = cgroup_stat['nr_subsys_cpuset']
        stat_kv_expected = 93
        self.assertEqual(stat_kv_value,stat_kv_expected, f'Expected {stat_kv_expected} kv-pairs; got {stat_kv_value}')

        # ----------
        # The bad
        cgroup, errors = CGroup.ingest_cgroup("data/bad/fs/cgroup", "cgroup", "TOP")
        
        # cgroup.controllers has an extra "comment" line       1
        # cgroup.stat is ok                                    0
        # cgroup.max.depth is missing                          1
        # cgroup.max.descendants is _wx_wx_wx (unable to read) 1
        # cpu.stat has bad formatting                          1
        #
        #                                               Total: 4
        errors_count = len(errors)
        errors_expected = 4
        errors_jsonified = json.dumps(errors, indent=2)
        self.assertEqual(errors_count,errors_expected, f'Expected {errors_expected} errors; got {errors_count}\n{errors_jsonified}')

        cgroup_controllers = cgroup['cgroup_controllers']
        controllers_count = len(cgroup_controllers)
        controllers_expected = 0
        self.assertEqual(controllers_count,controllers_expected, f'Expected {controllers_expected} controllers; got {controllers_count}')

        kvpairs = cgroup['cgroup_stat']
        kfpairs_count = len(kvpairs)
        stat_kv_expected = 22
        self.assertEqual(kfpairs_count,stat_kv_expected, f'Expected {stat_kv_expected} kv-pairs; got {kfpairs_count}')

        discovered_value = cgroup['cgroup_max_descendants']
        expected_value = ""
        self.assertEqual(discovered_value,expected_value, f'Expected [{expected_value}] string; got [{discovered_value}]')

        discovered_value = cgroup['cgroup_max_depth']
        expected_value = ""
        self.assertEqual(discovered_value,expected_value, f'Expected [{expected_value}] string; got [{discovered_value}]')

        kvpairs = cgroup['cpu_stat']
        kfpairs_count = len(kvpairs)
        kvpairs_expected = 0
        self.assertEqual(kfpairs_count, kvpairs_expected, f'Expected {kvpairs_expected} kv-pairs; got {kfpairs_count}')

    # ========================================================================
    # test_kvingest covers the ingest_stdkv() (static) method.
    def test_kvingest(self):

        # File not found
        with self.assertRaises(Exception):
            CGroup.ingest_stdkv("data/bad/fs/cgroup/cgroup.stat.nope")

        # One line (the last) does not conform to key-value format.
        # Has key-value-value
        with self.assertRaises(Exception):
            CGroup.ingest_stdkv("data/bad/fs/cgroup/cgroup.stat.1")

        # Last line is missing the EOL.
        kvlist = CGroup.ingest_stdkv("data/bad/fs/cgroup/cgroup.stat.2")

        items_found = len(kvlist)
        items_expected = 22
        self.assertEqual(items_found,items_expected, f'Expected {items_expected} kv-pairs; got {items_found}')

        # One line (the last) does not conform to key-value format.
        # Has key
        with self.assertRaises(Exception):
            CGroup.ingest_stdkv("data/bad/fs/cgroup/cgroup.stat.3")

# ============================================================================
if __name__ == '__main__':
    unittest.main()