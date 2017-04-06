"""

An event during an experiment

@author: Dror Dotan
@copyright: Copyright (c) 2017, Dror Dotan
"""

import numbers, re

import trajtracker
import trajtracker._utils as _u


# noinspection PyProtectedMember
class Event(trajtracker._TTrkObject):
    # todo: change example to a text box and trial starts


    #----------------------------------------------------
    def __init__(self, event_id, extends=None):
        """
        Constructor - invoked when you create a new object by writing Event()

        :param event_id: A string that uniquely identifies the event
        :type event_id: str
        :param extends: If this event extends another one (see details in :ref:`event-hierarchy`)
        :type extends: Event
        """
        super(Event, self).__init__()

        _u.validate_func_arg_type(self, "__init__", "extends", extends, Event, True)

        self._event_id = event_id
        self._offset = 0

        self._extended = False
        self._extends = extends
        if extends is not None:
            extends._extended = True


    #----------------------------------------------------
    @property
    def event_id(self):
        """
        The ID of this event (string)
        """
        return self._event_id


    #----------------------------------------------------
    @property
    def offset(self):
        """
        An offset (in seconds) relatively to the time the event occurred
        """
        return self._offset


    #----------------------------------------------------
    @property
    def extends(self):
        """The event that the present event extends (or None)"""
        return self._extends


    #----------------------------------------------------
    @property
    def event_hierarchy(self):
        """The present event, and all the events it extends"""

        result = []
        e = self
        while e is not None:
            result.append(e)
            e = e._extends

        return result


    #----------------------------------------------------
    def __add__(self, rhs):
        """Define a new event, in a time offset relatively to an existing event"""

        _u.validate_func_arg_type(self, "+", "right operand", rhs, numbers.Number)
        if rhs < 0:
            raise ValueError("trajtracker error: Invalid offset ({:}) for event {:}. Only events with positive offset are acceptable".format(
                rhs, self._event_id))

        new_event = Event(self._event_id)
        new_event._offset = self._offset + rhs
        return new_event


    #----------------------------------------------------
    @staticmethod
    def parse(text):
        """
        Parse a string into an event object. "None" is acceptable.
        """
        if not isinstance(text, str):
            raise ValueError("trajtracker error: invalid event format ({:}) - expecting a string value".format(text))

        if re.match('^\s*none\s*$', text.lower()):
            return None

        m = re.match('^\s*(\w+)\s*(\+\s*((\d+)|(\d*.\d+)))?\s*$', text)
        if m is None:
            raise ValueError("trajtracker error: invalid event format ({:}) - expecting event_id or event_id+offset".format(text))

        event = Event(m.group(1))
        if m.group(2) is not None:
            event += float(m.group(3))

        return event

    #----------------------------------------------------
    def __str__(self):
        if self._offset == 0:
            return self._event_id
        else:
            return "{:} + {:.3g}sec".format(self._event_id, self._offset)