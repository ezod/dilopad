  #   #               #
  #   #               #
### # # ### ### ### ###
# # # # # # # # # # # #
### # # ### ###  ## ###
            #
            #

"""\
Device module.

@author: Aaron Mavrinac
@contact: mavrinac@gmail.com
@license: GPL-3
"""

class Device(object):
    """\
    Device class.
    """
    _inputs = {}
    _outputs = {}

    def __init__(self):
        """\
        Constructor. Not to be instantiated directly.
        """
        if self.__class__ is Device:
            raise NotImplementedError('cannot instantiate an abstract device')

    @property
    def inputs(self):
        """\
        A list of inputs to this device.
        """
        return self._inputs.keys()

    @property
    def outputs(self):
        """\
        A list of output from this device.
        """
        return self._outputs.keys()

    def set_input(self, inputid, value):
        """\
        Set an input to a specified value.

        @param inputid: The input ID.
        @type inputid: C{str}
        @param value: The value to set.
        @type value: C{bool}
        """
        if not inputid in self.inputs:
            raise KeyError('device has no input %s' % inputid)
        self._inputs[inputid] = value
        self._update()

    def get_output(self, outputid):
        """\
        Get the value of an output.

        @param outputid: The output ID.
        @type outputid: C{str}
        """
        try:
            return self._outputs[outputid]
        except KeyError:
            raise KeyError('device has no output %s' % outputid)

    def _update(self):
        """\
        Update outputs based on inputs.
        """
        raise NotImplementedError('_update method must be overridden')
