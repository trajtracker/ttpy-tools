import unittest

import xml.etree.ElementTree as ET

import trajtracker
from trajtracker.movement import TrajectoryTracker
from ttrk_testing import DummyFileHandle


class TrajectoryTrackerForTesting(TrajectoryTracker):

    def _open_file(self, filename, mode):

        if mode == 'w':
            self._file_data = DummyFileHandle()

        return self._file_data



class TrajectoryTrackerTestCase(unittest.TestCase):

    #------------------------------------------------------------------
    def test_track(self):

        ttrk = TrajectoryTrackerForTesting()
        ttrk.enabled = True
        ttrk.init_output_file("stam", xy_precision=1, time_precision=1)

        ttrk.update_xyt((1, 1.5), 0.1)
        ttrk.update_xyt((2, 2.5), 0.2)
        ttrk.save_to_file(0)

        ttrk.reset()
        ttrk.enabled = True
        ttrk.update_xyt((12, 2.5), 0.2)
        ttrk.update_xyt((13, 3.5), 0.3)
        ttrk.save_to_file(1)

        self.assertEqual("trial,time,x,y\n0,0.1,1,1.5\n0,0.2,2,2.5\n1,0.2,12,2.5\n1,0.3,13,3.5\n", ttrk._file_data.data)

        xyt = ttrk.get_xyt()
        self.assertEqual(2, len(xyt))
        self.assertEqual((12,2.5,0.2), xyt[0])
        self.assertEqual((13,3.5,0.3), xyt[1])


    #------------------------------------------------------------------
    def test_track_active_inactive(self):

        ttrk = TrajectoryTrackerForTesting()
        ttrk.init_output_file("stam", xy_precision=1, time_precision=1)

        ttrk.update_xyt((1, 1.5), 0.1)
        ttrk.enabled = True
        ttrk.update_xyt((2, 2.5), 0.2)
        ttrk.update_xyt((3, 3.5), 0.3)
        ttrk.enabled = False
        ttrk.update_xyt((4, 4.5), 0.4)
        ttrk.save_to_file(0)

        self.assertEqual("trial,time,x,y\n0,0.2,2,2.5\n0,0.3,3,3.5\n", ttrk._file_data.data)

    #------------------------------------------------------------------
    def test_prec(self):

        ttrk = TrajectoryTrackerForTesting()
        ttrk.init_output_file("stam", xy_precision=2, time_precision=3)
        ttrk.enabled = True
        ttrk.update_xyt((0.2, 0.3), 0.1)
        ttrk.save_to_file(0)

        self.assertEqual("trial,time,x,y\n0,0.100,0.20,0.30\n", ttrk._file_data.data)

    #------------------------------------------------------------------
    def test_no_track_no_movement(self):

        ttrk = TrajectoryTrackerForTesting()
        ttrk.enabled = True
        ttrk.track_if_no_movement = False
        ttrk.init_output_file("stam", xy_precision=1, time_precision=1)

        ttrk.update_xyt((1, 1), 0.1)
        ttrk.update_xyt((1, 1), 0.2)
        ttrk.save_to_file(2)

        self.assertEqual("trial,time,x,y\n2,0.1,1,1\n", ttrk._file_data.data)


    #------------------------------------------------------------------
    def test_track_if_movement(self):

        ttrk = TrajectoryTrackerForTesting()
        ttrk.enabled = True
        ttrk.track_if_no_movement = True
        ttrk.init_output_file("stam", xy_precision=1, time_precision=1)

        ttrk.update_xyt((1, 1), 0.1)
        ttrk.update_xyt((1, 1), 0.2)
        ttrk.save_to_file(2)

        self.assertEqual("trial,time,x,y\n2,0.1,1,1\n2,0.2,1,1\n", ttrk._file_data.data)


    #------------------------------------------------------------------
    def test_non_numeric_time(self):
        ttrk = TrajectoryTrackerForTesting()
        try:
            ttrk.update_xyt((0.2, 0.3), "")
            self.fail("Succeeded tracking a non-numeric time")
        except(Exception):
            pass


    #------------------------------------------------------------------
    def test_negative_time(self):
        ttrk = TrajectoryTrackerForTesting()
        try:
            ttrk.update_xyt((0.2, 0.3), -1)
            self.fail("Succeeded tracking a negative time")
        except(Exception):
            pass

    #------------------------------------------------------------------
    def test_non_numeric_x(self):
        ttrk = TrajectoryTrackerForTesting()
        try:
            ttrk.update_xyt(("", 0.3), 0)
            self.fail("Succeeded tracking a non-numeric x coord")
        except(Exception):
            pass

    #------------------------------------------------------------------
    def test_non_numeric_y(self):
        ttrk = TrajectoryTrackerForTesting()
        try:
            ttrk.update_xyt((0.2, ""), 0.3)
            self.fail("Succeeded tracking a non-numeric y coord")
        except(Exception):
            pass

    # ==============================================================================
    #    Properties
    # ==============================================================================


    #------------------------------------------------------------------
    def test_set_enabled(self):
        trk = TrajectoryTracker()
        trk.enabled = True
        self.assertRaises(trajtracker.TypeError, lambda: TrajectoryTracker(enabled=""))
        self.assertRaises(trajtracker.TypeError, lambda: TrajectoryTracker(enabled=None))


    #------------------------------------------------------------------
    def test_set_track_if_no_movement(self):
        trk = TrajectoryTracker()
        trk.track_if_no_movement = True
        self.assertRaises(trajtracker.TypeError, lambda: TrajectoryTracker(track_if_no_movement=""))
        self.assertRaises(trajtracker.TypeError, lambda: TrajectoryTracker(track_if_no_movement=None))


if __name__ == '__main__':
    unittest.main()
