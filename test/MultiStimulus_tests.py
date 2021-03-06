import unittest

from expyriment.stimuli import Picture

import trajtracker as ttrk
from trajtracker.stimuli import MultiStimulus
from trajtracker.events import *



#--------------------------------------------------
class StimDbg(object):
    # noinspection PyMissingConstructor
    def __init__(self, text_id="dummy"):
        self._is_preloaded = False
        self._position = (0, 0)
        self._filename = "DebugPicture"
        self._text_id = text_id

    def present(self, clear=True, update=True, log_event_tag=None):
        pass

    def unload(self, keep_surface=False):
        pass

    def preload(self, inhibit_ogl_compress=False):
        self._is_preloaded = True

    @property
    def is_preloaded(self):
        return self._is_preloaded

    def __str__(self):
        return self._text_id



#===================================================================

class MultiStimulusTests(unittest.TestCase):

    def setUp(self):
        ttrk.log_to_console = True

    #----------------------------------------------------------------
    def test_create_empty(self):
        MultiStimulus()


    #----------------------------------------------------------------
    def test_set_available_pics(self):
        mp = MultiStimulus(available_stimuli=dict(a=StimDbg(), b=StimDbg()))

        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(available_stimuli=""))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(available_stimuli=dict(a=3)))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(available_stimuli=dict(a=None)))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(available_stimuli={1: StimDbg()}))

    #----------------------------------------------------------------
    def test_add_pict(self):
        mp = MultiStimulus()
        mp.add_stimulus('c', StimDbg())

        self.assertRaises(ttrk.TypeError, lambda: mp.add_stimulus('c', 3))
        self.assertRaises(ttrk.TypeError, lambda: mp.add_stimulus(3, StimDbg()))

    #----------------------------------------------------------------
    def test_set_shown_pics(self):
        MultiStimulus(available_stimuli=dict(a=StimDbg(), b=StimDbg()))
        MultiStimulus(shown_stimuli=['a', 'b'])
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(shown_stimuli=[1]))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(shown_stimuli=[None]))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(shown_stimuli=2))


    #---------------------------------------------------
    def test_set_position(self):
        mp = MultiStimulus(position=(10, 10))
        self.assertEqual((10, 10), mp.position)
        mp.position = (1, 2), (4, 5)
        mp.position = None

    def test_set_position_invalid(self):
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(position=(1,)))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(position=('a', 'b')))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(position='a'))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(position=['a']))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(position=[(1,)]))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(position=[('a', 'b')]))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(position=[None]))


    #==============================================================================
    #   Configure RSVP properties
    #==============================================================================

    #---------------------------------------------------
    def test_set_onset_time(self):
        rsvp = MultiStimulus(onset_time=(1, 2))
        self.assertEqual((1, 2), rsvp.onset_time)
        rsvp.onset_time = None

    def test_set_onset_time_invalid(self):
        self.assertRaises(ttrk.ValueError, lambda: MultiStimulus(onset_time=[-5]))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(onset_time=5))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(onset_time='hi'))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(onset_time=['hi']))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(onset_time=[]))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(onset_time=[None]))

    #---------------------------------------------------
    def test_set_duration(self):
        rsvp = MultiStimulus(duration=(1, 2))
        self.assertEqual((1, 2), rsvp.duration)
        rsvp.duration = 5
        rsvp.duration = None

    def test_set_duration_invalid(self):
        self.assertRaises(ttrk.ValueError, lambda: MultiStimulus(duration=[-5]))
        self.assertRaises(ttrk.ValueError, lambda: MultiStimulus(duration=[0]))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(duration='hi'))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(duration=['hi']))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(duration=[]))
        self.assertRaises(ttrk.TypeError, lambda: MultiStimulus(duration=[None]))

    #==============================================================================
    #   Validation function for RSVP properties
    #==============================================================================

    def test_validate_ok(self):
        self._create_good_multistim()._validate()

    #---------------------------------------------------
    # noinspection PyTypeChecker
    def _create_good_multistim(self, available_stimuli=None,
                               shown_stimuli=('a', 'b'), position=(0, 0),
                               onset_time=(0, 1, 2), duration=1.0, start_event=TRIAL_STARTED):

        if available_stimuli is None:
            available_stimuli = dict(a=StimDbg(), b=StimDbg())

        return MultiStimulus(available_stimuli=available_stimuli, shown_stimuli=shown_stimuli,
                             position=position, onset_time=onset_time, duration=duration,
                             onset_event=start_event)


    #---------------------------------------------------
    # noinspection PyTypeChecker
    def test_validate_bad_shown_pics(self):
        mp = self._create_good_multistim(shown_stimuli=('c',))
        self.assertRaises(ttrk.ValueError, lambda: mp._validate())

    #---------------------------------------------------
    # noinspection PyTypeChecker
    def test_validate_bad_position(self):
        self.assertRaises(ttrk.ValueError, lambda: self._create_good_multistim(position=None)._validate())
        self.assertRaises(ttrk.ValueError, lambda: self._create_good_multistim(position=((10, 10),))._validate())

    #---------------------------------------------------
    # noinspection PyTypeChecker
    def test_validate_bad_duration(self):
        self.assertRaises(ttrk.ValueError, lambda: self._create_good_multistim(duration=None)._validate())
        self.assertRaises(ttrk.ValueError, lambda: self._create_good_multistim(duration=(10,))._validate())

    #==============================================================================
    #   Working without event manager
    #==============================================================================

    #---------------------------------------------------
    def test_noevents_one_stim_onset_time0(self):
        rsvp = self._create_good_multistim(shown_stimuli=['a'], onset_time=[0], duration=1)
        rsvp.init_for_trial()
        self.assertEqual([False], rsvp.stim_visibility)
        self.assertEqual(False, rsvp._stimuli[0].visible)
        rsvp.start_showing(10)
        self.assertEqual([True], rsvp.stim_visibility)
        self.assertEqual(True, rsvp._stimuli[0].visible)
        rsvp.update_display(10.99)
        self.assertEqual([True], rsvp.stim_visibility)
        self.assertEqual(True, rsvp._stimuli[0].visible)
        rsvp.update_display(11)
        self.assertEqual([False], rsvp.stim_visibility)
        self.assertEqual(False, rsvp._stimuli[0].visible)
        rsvp.update_display(20)
        self.assertEqual([False], rsvp.stim_visibility)


    #---------------------------------------------------
    def test_noevents_one_stim_onset_time_gt_0(self):
        rsvp = self._create_good_multistim(shown_stimuli=['a'], onset_time=[1], duration=1)
        rsvp.init_for_trial()
        rsvp.start_showing(10)
        self.assertEqual([False], rsvp.stim_visibility)
        rsvp.update_display(10.5)
        self.assertEqual([False], rsvp.stim_visibility)
        rsvp.update_display(11)
        self.assertEqual([True], rsvp.stim_visibility)
        rsvp.update_display(11.99)
        self.assertEqual([True], rsvp.stim_visibility)
        rsvp.update_display(12)
        self.assertEqual([False], rsvp.stim_visibility)

    #---------------------------------------------------
    def test_noevents_two_stim_onset_time(self):
        rsvp = self._create_good_multistim(shown_stimuli=['a', 'b'], onset_time=[0, 3], duration=1)

        rsvp.init_for_trial()
        self.assertEqual([False, False], rsvp.stim_visibility)
        self.assertEqual(False, rsvp._stimuli[0].visible)
        self.assertEqual(False, rsvp._stimuli[1].visible)

        rsvp.start_showing(10)
        self.assertEqual([True, False], rsvp.stim_visibility)
        self.assertEqual(True, rsvp._stimuli[0].visible)
        self.assertEqual(False, rsvp._stimuli[1].visible)

        rsvp.update_display(10.99)
        self.assertEqual([True, False], rsvp.stim_visibility)
        self.assertEqual(True, rsvp._stimuli[0].visible)
        self.assertEqual(False, rsvp._stimuli[1].visible)

        rsvp.update_display(11)
        self.assertEqual([False, False], rsvp.stim_visibility)
        self.assertEqual(False, rsvp._stimuli[0].visible)
        self.assertEqual(False, rsvp._stimuli[1].visible)

        rsvp.update_display(13)
        self.assertEqual([False, True], rsvp.stim_visibility)
        self.assertEqual(False, rsvp._stimuli[0].visible)
        self.assertEqual(True, rsvp._stimuli[1].visible)

        rsvp.update_display(13.99)
        self.assertEqual([False, True], rsvp.stim_visibility)
        self.assertEqual(False, rsvp._stimuli[0].visible)
        self.assertEqual(True, rsvp._stimuli[1].visible)

        rsvp.update_display(14)
        self.assertEqual([False, False], rsvp.stim_visibility)
        self.assertEqual(False, rsvp._stimuli[0].visible)
        self.assertEqual(False, rsvp._stimuli[1].visible)


    #---------------------------------------------------
    def test_noevents_last_stim_remains(self):
        rsvp = self._create_good_multistim(shown_stimuli=['a', 'b'], onset_time=[0, 3], duration=1)
        rsvp.last_stimulus_remains = True

        rsvp.init_for_trial()
        rsvp.start_showing(10)
        rsvp.update_display(30)
        self.assertEqual([False, True], rsvp.stim_visibility)
        self.assertEqual(True, rsvp._stimuli[1].visible)


    #---------------------------------------------------
    def test_noevents_cleanup(self):
        rsvp = self._create_good_multistim(shown_stimuli=['a'], onset_time=[0, 3], duration=1)

        rsvp.init_for_trial()
        rsvp.start_showing(10)
        rsvp.update_display(10.5)

        self.assertEqual(1, len(rsvp._show_hide_operations))  # SHOW was performed; only the HIDE operation remains
        rsvp.update_display(15)
        self.assertEqual(0, len(rsvp._show_hide_operations))  # No operation remained

        rsvp.init_for_trial()
        self.assertEqual(2, len(rsvp._show_hide_operations))  # Both SHOW and HIDE


    #==============================================================================
    #   Working with event manager
    #==============================================================================

    #---------------------------------------------------
    def test_events_one_stim_onset_time0(self):
        em = EventManager()
        em.log_level = ttrk.log_trace
        rsvp = self._create_good_multistim(shown_stimuli=['a'], onset_time=[0], duration=1)
        em.register(rsvp)

        em.dispatch_event(TRIAL_INITIALIZED, time_in_trial=1, time_in_session=1)
        self.assertEqual([False], rsvp.stim_visibility)
        self.assertEqual(False, rsvp._stimuli[0].visible)

        em.dispatch_event(TRIAL_STARTED, time_in_trial=10, time_in_session=10)
        self.assertEqual([True], rsvp.stim_visibility)
        self.assertEqual(True, rsvp._stimuli[0].visible)

        em.on_frame(time_in_trial=10.99, time_in_session=10.99)
        self.assertEqual([True], rsvp.stim_visibility)
        self.assertEqual(True, rsvp._stimuli[0].visible)

        em.on_frame(time_in_trial=11, time_in_session=11)
        self.assertEqual([False], rsvp.stim_visibility)
        self.assertEqual(False, rsvp._stimuli[0].visible)

        em.on_frame(time_in_trial=20, time_in_session=20)
        self.assertEqual([False], rsvp.stim_visibility)


    #---------------------------------------------------
    def test_events_one_stim_onset_time_gt_0(self):
        em = EventManager()
        em.log_level = ttrk.log_trace
        rsvp = self._create_good_multistim(shown_stimuli=['a'], onset_time=[1], duration=1)
        em.register(rsvp)

        em.dispatch_event(TRIAL_INITIALIZED, time_in_trial=1, time_in_session=1)
        self.assertEqual([False], rsvp.stim_visibility)

        em.dispatch_event(TRIAL_STARTED, time_in_trial=0, time_in_session=10)
        self.assertEqual([False], rsvp.stim_visibility)

        em.on_frame(time_in_trial=0, time_in_session=10.99)
        self.assertEqual([False], rsvp.stim_visibility)

        em.on_frame(time_in_trial=0, time_in_session=11)
        self.assertEqual([True], rsvp.stim_visibility)

        em.on_frame(time_in_trial=0, time_in_session=11.99)
        self.assertEqual([True], rsvp.stim_visibility)

        em.on_frame(time_in_trial=0, time_in_session=12)
        self.assertEqual([False], rsvp.stim_visibility)

        em.on_frame(time_in_trial=0, time_in_session=20)
        self.assertEqual([False], rsvp.stim_visibility)

    #---------------------------------------------------
    def test_events_two_stim_onset_time(self):
        em = EventManager()
        em.log_level = ttrk.log_trace
        rsvp = self._create_good_multistim(shown_stimuli=['a', 'b'], onset_time=[0, 3], duration=1)
        em.register(rsvp)

        em.dispatch_event(TRIAL_INITIALIZED, time_in_trial=1, time_in_session=1)
        self.assertEqual([False, False], rsvp.stim_visibility)

        em.dispatch_event(TRIAL_STARTED, time_in_trial=0, time_in_session=10)
        self.assertEqual([True, False], rsvp.stim_visibility)

        em.on_frame(time_in_trial=0, time_in_session=10.99)
        self.assertEqual([True, False], rsvp.stim_visibility)

        em.on_frame(time_in_trial=0, time_in_session=11)
        self.assertEqual([False, False], rsvp.stim_visibility)

        em.on_frame(time_in_trial=0, time_in_session=13)
        self.assertEqual([False, True], rsvp.stim_visibility)

        em.on_frame(time_in_trial=0, time_in_session=13.99)
        self.assertEqual([False, True], rsvp.stim_visibility)

        em.on_frame(time_in_trial=0, time_in_session=14)
        self.assertEqual([False, False], rsvp.stim_visibility)

    #---------------------------------------------------
    def test_events_last_stim_remains(self):
        em = EventManager()
        em.log_level = ttrk.log_trace
        rsvp = self._create_good_multistim(shown_stimuli=['a', 'b'], onset_time=[0, 3], duration=1)
        rsvp.last_stimulus_remains = True
        em.register(rsvp)

        em.dispatch_event(TRIAL_INITIALIZED, time_in_trial=1, time_in_session=1)
        em.dispatch_event(TRIAL_STARTED, time_in_trial=0, time_in_session=10)
        em.on_frame(time_in_trial=0, time_in_session=30)
        self.assertEqual([False, True], rsvp.stim_visibility)
        self.assertEqual(True, rsvp._stimuli[1].visible)


    #---------------------------------------------------
    def test_events_simultaneous_events(self):
        em = EventManager()
        em.log_level = ttrk.log_trace
        rsvp = self._create_good_multistim(shown_stimuli=['a', 'b'], onset_time=[1, 0], duration=2)
        em.register(rsvp)

        em.dispatch_event(TRIAL_INITIALIZED, time_in_trial=1, time_in_session=1)
        self.assertEqual([False, False], rsvp.stim_visibility)

        em.dispatch_event(TRIAL_STARTED, time_in_trial=0, time_in_session=10)
        self.assertEqual([False, True], rsvp.stim_visibility)

        em.on_frame(time_in_trial=0, time_in_session=11)
        self.assertEqual([True, True], rsvp.stim_visibility)

        em.on_frame(time_in_trial=0, time_in_session=12)
        self.assertEqual([True, False], rsvp.stim_visibility)

        em.on_frame(time_in_trial=0, time_in_session=13)
        self.assertEqual([False, False], rsvp.stim_visibility)


    #---------------------------------------------------
    def test_events_cancel(self):
        em = EventManager()
        em.log_level = ttrk.log_trace
        rsvp = self._create_good_multistim(shown_stimuli=['a', 'b'], onset_time=[1, 0], duration=2)
        em.register(rsvp)

        em.dispatch_event(TRIAL_INITIALIZED, time_in_trial=1, time_in_session=1)
        self.assertEqual([False, False], rsvp.stim_visibility)

        em.dispatch_event(TRIAL_STARTED, time_in_trial=0, time_in_session=10)
        self.assertEqual([False, True], rsvp.stim_visibility)

        em.dispatch_event(TRIAL_SUCCEEDED, time_in_trial=0, time_in_session=10.5)

        em.on_frame(time_in_trial=0, time_in_session=11)
        self.assertEqual([False, False], rsvp.stim_visibility)

        em.on_frame(time_in_trial=0, time_in_session=12)
        self.assertEqual([False, False], rsvp.stim_visibility)

        em.on_frame(time_in_trial=0, time_in_session=13)
        self.assertEqual([False, False], rsvp.stim_visibility)


    #==============================================================================
    #   Callbacks
    #==============================================================================

    #----------------------------------------------------
    def test_callback_1(self):
        a = StimDbg(text_id="a")
        b = StimDbg(text_id="b")
        ms = self._create_good_multistim(available_stimuli=dict(a=a, b=b),
                                         shown_stimuli=['a', 'b'], onset_time=[0, 0.2], duration=0.1)
        container = StimulusContainerDbg()
        ms._container = container

        cbk = MultiStimDbgCallback()
        ms.register_onset_offset_callback_func(cbk)

        ms.init_for_trial()
        ms.start_showing(0)
        container.present()
        self.assertEqual(True, a.visible)  # Just a sanity check - to make sure it worked
        self.assertEqual(1, cbk.n_times_called)
        self.assertEqual(0, cbk.stim_number)
        self.assertEqual(True, cbk.visible)

        ms.update_display(0.08)
        self.assertEqual(1, cbk.n_times_called)

        ms.update_display(0.1)
        container.present()
        self.assertEqual(False, a.visible)  # sanity check
        self.assertEqual(2, cbk.n_times_called)
        self.assertEqual(0, cbk.stim_number)
        self.assertEqual(False, cbk.visible)

        ms.update_display(0.2)
        container.present()
        self.assertEqual(True, b.visible)  # sanity check
        self.assertEqual(3, cbk.n_times_called)
        self.assertEqual(1, cbk.stim_number)
        self.assertEqual(True, cbk.visible)


    #----------------------------------------------------
    def test_callback_offset_and_onset_at_same_time(self):
        a = StimDbg(text_id="a")
        b = StimDbg(text_id="b")
        ms = self._create_good_multistim(available_stimuli=dict(a=a, b=b),
                                         shown_stimuli=['a', 'b'], onset_time=[0, 0.1], duration=0.1)
        container = StimulusContainerDbg()
        ms._container = container

        cbk = MultiStimDbgCallback()
        ms.register_onset_offset_callback_func(cbk)

        ms.init_for_trial()
        ms.start_showing(0)
        container.present()
        self.assertEqual(True, a.visible)  # Just a sanity check - to make sure it worked
        self.assertEqual(1, cbk.n_times_called)

        ms.update_display(0.1)
        container.present()
        self.assertEqual(False, a.visible)  # sanity check
        self.assertEqual(True, b.visible)  # sanity check
        self.assertEqual(3, cbk.n_times_called)



class MultiStimDbgCallback(object):

    def __init__(self):
        self.n_times_called = 0

    def __call__(self, ms, stim_number, visible, time):
        self.ms = ms
        self.stim_number = stim_number
        self.visible = visible
        self.time = time
        self.n_times_called += 1


class StimulusContainerDbg(ttrk.stimuli.StimulusContainer):

    def present(self, clear=True, update=True):
        self._invoke_callbacks([])


if __name__ == '__main__':
    unittest.main()
