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
    def __init__(self):
        """\
        Constructor. Not to be instantiated directly.
        """
        self._inputs = {}
        self._outputs = {}
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
        A list of outputs from this device.
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
            raise KeyError('no input %s' % inputid)
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
            raise KeyError('no output %s' % outputid)

    def _update(self):
        """\
        Update outputs based on inputs.
        """
        raise NotImplementedError('_update method must be overridden')


class Circuit(Device):
    """\
    Circuit class. Hierarchical container for Device objects which itself
    exposes the Device API.
    """
    def __init__(self):
        super(Circuit, self).__init__()
        self._devices = {}
        self._connections = {}
        self._cached_outputs = {}

    @property
    def inputs(self):
        """\
        A list of inputs to this circuit. By default, the set of inputs is
        generated as all unconnected inputs of the circuit's devices.
        """
        return ['%s.%s' % (deviceid, inputid) \
            for deviceid in self._devices.keys() \
            for inputid in self._devices[deviceid].inputs \
            if not self._connections.has_key((deviceid, inputid))]

    @property
    def outputs(self):
        """\
        A list of outputs from this circuit. By default, the set of outputs is
        generated as all outputs of the circuit's devices.
        """
        return ['%s.%s' % (deviceid, outputid) \
            for deviceid in self._devices.keys() \
            for outputid in self._devices[deviceid].outputs]

    def add(self, deviceid, device):
        """\
        Add a device to the circuit.

        @param deviceid: An ID for the device.
        @type deviceid: C{str}
        @param device: The device to add to the circuit.
        @type device: L{Device}
        """
        if not isinstance(device, Device):
            raise TypeError('not a device')
        if self._devices.has_key(deviceid):
            raise ValueError('duplicate device ID')
        self._devices[deviceid] = device
        for outputid in device.outputs:
            self._cached_outputs[(deviceid, outputid)] = \
                device.get_output(outputid)

    def remove(self, deviceid):
        """\
        Remove a device from the circuit and delete all of its connections and
        cached outputs.

        @param deviceid: The ID of the device to remove.
        @type deviceid: C{str}
        """
        for connection in self._connections.keys():
            if connection.startswith(deviceid):
                del self._connections[connection]
            elif self._connections[connection].startswith(deviceid):
                del self._connections[connection]
        for cached_output in self._cached_outputs.keys():
            if cached_output[0] == deviceid:
                del self._cached_outputs[cached_output]
        del self._devices[deviceid]

    def connect(self, srcid, outputid, dstid, inputid):
        """\
        Connect the output of a device in this circuit to the input of another
        device in this circuit. If the input is already connected, this will
        silently replace the previous connection.

        @param srcid: The ID of the source device.
        @param outputid: The output ID from the source device.
        @param dstid: The ID of the destination device.
        @param inputid: The input ID from the destination device.
        """
        try:
            if outputid not in self._devices[srcid].outputs \
            or inputid not in self._devices[dstid].inputs:
                raise KeyError('invalid output/input')
        except KeyError:
            raise KeyError('invalid device')
        self._connections[(dstid, inputid)] = (srcid, outputid)
        self._devices[dstid].set_input(inputid,
            self._devices[srcid].get_output(outputid))
        self._update()

    def disconnect(self, deviceid, inputid):
        """\
        Disconnect an input.
        """
        del self._connections[(deviceid, inputid)]

    def set_input(self, inputid, value):
        """\
        Set an input to a specified value.

        @param inputid: The input ID.
        @type inputid: C{str}
        @param value: The value to set.
        @type value: C{bool}
        """
        if not inputid in self.inputs:
            raise KeyError('no input %s' % inputid)
        deviceid = inputid.split('.')[0]
        inputid = '.'.join(inputid.split('.')[1:])
        self._devices[deviceid].set_input(inputid, value)
        self._update()

    def get_output(self, outputid):
        """\
        Get the value of an output.

        @param outputid: The output ID.
        @type outputid: C{str}
        """
        deviceid = outputid.split('.')[0]
        outputid = '.'.join(outputid.split('.')[1:])
        try:
            return self._devices[deviceid].get_output(outputid)
        except KeyError:
            raise KeyError('no output %s.%s' % (deviceid, outputid))

    def _update(self):
        """\
        Update outputs based on inputs.
        """
        count = 0
        change = True
        while change:
            count += 1
            change = False
            for cached_output in self._cached_outputs.keys():
                if self.get_output('%s.%s' % cached_output) != \
                self._cached_outputs[cached_output]:
                    self._cached_outputs[cached_output] = \
                        not self._cached_outputs[cached_output]
                    for connection in self._connections.keys():
                        if self._connections[connection] == cached_output:
                            change = True
                            self._devices[connection[0]].set_input(\
                                connection[1],
                                self._cached_outputs[cached_output])
            if count > 10:
                raise RuntimeError('update loop depth exceeded')
