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

from ..device import Device

class NOTGate(Device):
    """\
    NOT gate class.
    """
    def __init__(self):
        """\
        Constructor.
        """
        super(NOTGate, self).__init__()
        self._inputs = {'a': False}
        self._outputs = {'q': True}

    def _update(self):
        """\
        Update outputs based on inputs.
        """
        if self._inputs['a']:
            self._outputs['q'] = False
        else:
            self._outputs['q'] = True


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
        if self._inputs['a'] and self._inputs['b']:
            self._outputs['q'] = True
        else:
            self._outputs['q'] = False


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
        if self._inputs['a'] or self._inputs['b']:
            self._outputs['q'] = True
        else:
            self._outputs['q'] = False


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
        if self._inputs['a'] and self._inputs['b']:
            self._outputs['q'] = False
        else:
            self._outputs['q'] = True


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
        if self._inputs['a'] or self._inputs['b']:
            self._outputs['q'] = False
        else:
            self._outputs['q'] = True


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
        if self._inputs['a'] or self._inputs['b'] \
        and not (self._inputs['a'] and self._inputs['b']):
            self._outputs['q'] = True
        else:
            self._outputs['q'] = False


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
        if self._inputs['a'] or self._inputs['b'] \
        and not (self._inputs['a'] and self._inputs['b']):
            self._outputs['q'] = False
        else:
            self._outputs['q'] = True
