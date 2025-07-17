#!/usr/bin/python3

from cgtool.CGroup import CGroup

import unittest


class TestCGroup(unittest.TestCase):

    def test_controllers(self):

        # STUB: Test for raised exceptions
        # STUB: Write tests that will raise exceptions

        controllers = CGroup.ingest_controllers("data/sys/fs/cgroup/cgroup.controllers")
        controllers_count = len(controllers)
        controllers_expected = 9
        self.assertEqual(controllers_count,controllers_expected, f'Expected {controllers_expected} controllers; got {controllers_count}')



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



if __name__ == '__main__':
    unittest.main()