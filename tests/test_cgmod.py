#!/usr/bin/python3

from cgtool.CGroup import CGroup

import unittest


class TestCGroup(unittest.TestCase):

    def test_controllers(self):
      
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





    def test_cgingest(self):
        cgroup, errors = CGroup.ingest_cgroup("data/sys/fs/cgroup", "cgroup", "TOP")
        
        errors_count = len(errors)
        errors_expected = 0
        self.assertEqual(errors_count,errors_expected, f'Expected {errors_expected} controllers; got {errors_count}')

        cgroup_controllers = cgroup['cgroup_controllers']
        controllers_count = len(cgroup_controllers)
        controllers_expected = 9
        self.assertEqual(controllers_count,controllers_expected, f'Expected {controllers_expected} controllers; got {controllers_count}')

        cgroup_stat = cgroup['cgroup_stat']
        stat_kv_count = len(cgroup_stat)
        stat_kv_expected = 22
        self.assertEqual(stat_kv_count,stat_kv_expected, f'Expected {stat_kv_expected} controllers; got {stat_kv_count}')

        #nr_subsys_cpuset 93
        stat_kv_value = cgroup_stat['nr_subsys_cpuset']
        stat_kv_expected = 93
        self.assertEqual(stat_kv_value,stat_kv_expected, f'Expected {stat_kv_expected} controllers; got {stat_kv_value}')

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

   


if __name__ == '__main__':
    unittest.main()