  #   #               #
  #   #               #
### # # ### ### ### ###
# # # # # # # # # # # #
### # # ### ###  ## ###
            #
            #

"""\
Basic devices.

@author: Aaron Mavrinac
@contact: mavrinac@gmail.com
@license: GPL-3
"""

from ..device import Device


class Logic0(Device):
    """\
    Logic zero.
    """
    def __init__(self, pos=(0, 0)):
        """\
        Constructor.

        @param pos: The position of this device.
        @type pos: C{tuple} of C{int}
        """
        super(Logic0, self).__init__(pos=pos)
        self._outputs = {'q': False}

    def _update(self):
        pass


class Logic1(Device):
    """\
    Logic one.
    """
    def __init__(self, pos=(0, 0)):
        """\
        Constructor.

        @param pos: The position of this device.
        @type pos: C{tuple} of C{int}
        """
        super(Logic1, self).__init__(pos=pos)
        self._outputs = {'q': True}

    def _update(self):
        """\
        Update outputs based on inputs.
        """
        pass


class Buffer(Device):
    """\
    Buffer/node device class.
    """
    def __init__(self, pos=(0, 0)):
        """\
        Constructor.

        @param pos: The position of this device.
        @type pos: C{tuple} of C{int}
        """
        super(Buffer, self).__init__(pos=pos)
        self._inputs = {'a': False}
        self._outputs = {'q': True}

    def _update(self):
        """\
        Update outputs based on inputs.
        """
        self._outputs['q'] = self._inputs['a']


class Inverter(Device):
    """\
    Inverter (NOT gate) class.
    """
    def __init__(self, pos=(0, 0)):
        """\
        Constructor.

        @param pos: The position of this device.
        @type pos: C{tuple} of C{int}
        """
        super(Inverter, self).__init__(pos=pos)
        self._inputs = {'a': False}
        self._outputs = {'q': True}

    def _update(self):
        """\
        Update outputs based on inputs.
        """
        self._outputs['q'] = not self._inputs['a']


class Sender(Buffer):
    """\
    Sender class.
    """
    outputs = []

    def __init__(self, pos=(0, 0)):
        """\
        Constructor.

        @param pos: The position of this device.
        @type pos: C{tuple} of C{int}
        """
        super(Sender, self).__init__(pos=pos)
        self._receiver = None

    @property
    def receiver(self):
        """\
        The associated receiver.
        """
        return self._receiver

    @receiver.setter
    def receiver(self, value):
        """\
        Set the associated receiver.
        """
        if not isinstance(value, Receiver):
            raise TypeError('invalid receiver')
        if self._receiver:
            self._receiver._sender = None
        self._receiver = value
        self._receiver._sender = self

    @receiver.deleter
    def receiver(self):
        """\
        Unset the associated receiver.
        """
        if self._receiver:
            self._receiver._sender = None
            self._receiver = None

    def _update(self):
        """\
        Update outputs based on inputs. Also update the associated receiver if
        it has been set.
        """
        super(Sender, self)._update()
        if self._receiver:
            self._receiver._inputs['a'] = self._outputs['q']
            self._receiver._update()


class Receiver(Buffer):
    """\
    Receiver class.
    """
    inputs = []

    def __init__(self, pos=(0, 0)):
        """\
        Constructor.

        @param pos: The position of this device.
        @type pos: C{tuple} of C{int}
        """
        super(Receiver, self).__init__(pos=pos)
        self._sender = None

    @property
    def sender(self):
        """\
        The associated sender.
        """
        return self._sender
