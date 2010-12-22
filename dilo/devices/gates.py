  #   #               #
  #   #               #
### # # ### ### ### ###
# # # # # # # # # # # #
### # # ### ###  ## ###
            #
            #

"""\
Basic logic gates.

@author: Aaron Mavrinac
@contact: mavrinac@gmail.com
@license: GPL-3
"""

from functools import reduce

from ..device import Device


class ANDGate(Device):
    """\
    AND gate class.
    """
    def __init__(self):
        """\
        Constructor.
        """
        super(ANDGate, self).__init__()
        self._inputs = {'a': False, 'b': False}
        self._outputs = {'q': False}

    def _update(self):
        """\
        Update outputs based on inputs.
        """
        self._outputs['q'] = all(self._inputs.values())


class ORGate(Device):
    """\
    OR gate class.
    """
    def __init__(self):
        """\
        Constructor.
        """
        super(ORGate, self).__init__()
        self._inputs = {'a': False, 'b': False}
        self._outputs = {'q': False}

    def _update(self):
        """\
        Update outputs based on inputs.
        """
        self._outputs['q'] = any(self._inputs.values())


class NANDGate(Device):
    """\
    NAND gate class.
    """
    def __init__(self):
        """\
        Constructor.
        """
        super(NANDGate, self).__init__()
        self._inputs = {'a': False, 'b': False}
        self._outputs = {'q': False}

    def _update(self):
        """\
        Update outputs based on inputs.
        """
        self._outputs['q'] = not all(self._inputs.values())


class NORGate(Device):
    """\
    NOR gate class.
    """
    def __init__(self):
        """\
        Constructor.
        """
        super(NORGate, self).__init__()
        self._inputs = {'a': False, 'b': False}
        self._outputs = {'q': False}

    def _update(self):
        """\
        Update outputs based on inputs.
        """
        self._outputs['q'] = not any(self._inputs.values())


class XORGate(Device):
    """\
    XOR gate class.
    """
    def __init__(self):
        """\
        Constructor.
        """
        super(XORGate, self).__init__()
        self._inputs = {'a': False, 'b': False}
        self._outputs = {'q': False}

    def _update(self):
        """\
        Update outputs based on inputs.
        """
        self._outputs['q'] = reduce(lambda a, b: any((a, b)) \
                             and not all((a, b)), self._inputs.values())


class XNORGate(Device):
    """\
    XNOR gate class.
    """
    def __init__(self):
        """\
        Constructor.
        """
        super(XNORGate, self).__init__()
        self._inputs = {'a': False, 'b': False}
        self._outputs = {'q': False}

    def _update(self):
        """\
        Update outputs based on inputs.
        """
        self._outputs['q'] = not reduce(lambda a, b: any((a, b)) \
                             and not all((a, b)), self._inputs.values())
