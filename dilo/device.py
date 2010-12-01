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

    def apply_inputs(self, values):
        """\
        Apply a set of values to the inputs.

        @param values: The values to apply, keyed by input ID.
        @type values: C{dict} of C{bool}
        """
        for inputid in values.keys():
            self.set_input(inputid, values[inputid])

    def _update(self):
        """\
        Update outputs based on inputs.
        """
        raise NotImplementedError('_update method must be overridden')


class Logic0(Device):
    """\
    Logic zero.
    """
    def __init__(self):
        """\
        Constructor.
        """
        super(Logic0, self).__init__()
        self._outputs = {'q': False}

    def _update(self):
        pass


class Logic1(Device):
    """\
    Logic one.
    """
    def __init__(self):
        """\
        Constructor.
        """
        super(Logic1, self).__init__()
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
    def __init__(self):
        """\
        Constructor.
        """
        super(Buffer, self).__init__()
        self._inputs = {'a': False}
        self._outputs = {'q': True}

    def _update(self):
        """\
        Update outputs based on inputs.
        """
        self._outputs['q'] = self._inputs['a']


class Sender(Buffer):
    """\
    Sender class.
    """
    outputs = {}

    def __init__(self):
        """\
        Constructor.
        """
        super(Sender, self).__init__()
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
    inputs = {}

    def __init__(self):
        """\
        Constructor.
        """
        super(Receiver, self).__init__()
        self._sender = None

    @property
    def sender(self):
        """\
        The associated sender.
        """
        return self._sender


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

    def _internal_inputs(self):
        """\
        Return all unconnected inputs of the circuit's devices.
        """
        return ['%s.%s' % (deviceid, inputid) \
            for deviceid in self._devices.keys() \
            for inputid in self._devices[deviceid].inputs \
            if not self._connections.has_key((deviceid, inputid))]
    
    def _internal_outputs(self):
        """\
        Return all outputs of the circuit's devices.
        """
        return ['%s.%s' % (deviceid, outputid) \
            for deviceid in self._devices.keys() \
            for outputid in self._devices[deviceid].outputs]
        
    @property
    def inputs(self):
        """\
        A list of inputs to this circuit. By default, the set of inputs is
        generated as all unconnected inputs of the circuit's devices.
        """
        if len(self._inputs):
            return self._inputs.keys()
        else:
            return self._internal_inputs()

    @property
    def outputs(self):
        """\
        A list of outputs from this circuit. By default, the set of outputs is
        generated as all outputs of the circuit's devices.
        """
        if len(self._outputs):
            return self._outputs.keys()
        else:
            return self._internal_outputs()

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
        Remove a device from the circuit and delete all of its connections,
        cached outputs, and labels.

        @param deviceid: The ID of the device to remove.
        @type deviceid: C{str}
        """
        # delete connections
        for connection in self._connections.keys():
            if connection.startswith(deviceid):
                del self._connections[connection]
            elif self._connections[connection].startswith(deviceid):
                del self._connections[connection]
        # delete cached outputs
        for cached_output in self._cached_outputs.keys():
            if cached_output[0] == deviceid:
                del self._cached_outputs[cached_output]
        # delete labels
        for inputid in self._devices[deviceid].inputs:
            for label in self._inputs.keys():
                self._inputs[label].discard(inputid)
                if not len(self._inputs[label]):
                    del self._inputs[label]
        for outputid in self._devices[deviceid].outputs:
            for label in self._outputs.keys():
                if self._outputs[label] == outputid:
                    del self._outputs[label]
        # delete device
        del self._devices[deviceid]

    def connect(self, srcid, outputid, dstid, inputid):
        """\
        Connect the output of a device in this circuit to the input of another
        device in this circuit. If the input is already connected, this will
        silently replace the previous connection. If the input is assigned to a
        label, this will silently discard the label.

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
        for label in self._inputs.keys():
            self._inputs[label].discard('%s.%s' % (dstid, inputid))
            if not len(self._inputs[label]):
                del self._inputs[label]
        self._devices[dstid].set_input(inputid,
            self._devices[srcid].get_output(outputid))
        self._update()

    def disconnect(self, deviceid, inputid):
        """\
        Disconnect an input.
        """
        del self._connections[(deviceid, inputid)]

    def label_inputs(self, label, dstinputs):
        """\
        Create a transparent input alias for a set of inputs.

        @param label: The label to assign the new input alias.
        @type label: C{str}
        @param dstinputs: A set of inputs to assign to the alias.
        @type dstinputs: C{set} of C{str}
        """
        for dstinput in dstinputs:
            if dstinput not in self._internal_inputs():
                raise KeyError('invalid input %s' % dstinput)
        self._inputs[label] = set(dstinputs)

    def label_output(self, label, srcoutput):
        """\
        Create a transparent input alias for an output.

        @param label: The label to assign the new output alias.
        @type label: C{str}
        @param srcoutputs: The output to assign to the alias.
        @type srcoutput: C{str}
        """
        if srcoutput not in self._internal_outputs():
            raise KeyError('invalid output %s' % srcoutput)
        self._outputs[label] = srcoutput

    def set_input(self, inputid, value, internal=False):
        """\
        Set an input to a specified value.

        @param inputid: The input ID.
        @type inputid: C{str}
        @param value: The value to set.
        @type value: C{bool}
        """
        if not internal and not inputid in self.inputs:
            raise KeyError('no input %s' % inputid)
        if not internal and len(self._inputs):
            for dstinput in self._inputs[inputid]:
                self.set_input(dstinput, value, internal=True)
        else:
            deviceid = inputid.split('.')[0]
            inputid = '.'.join(inputid.split('.')[1:])
            self._devices[deviceid].set_input(inputid, value)
        self._update()

    def get_output(self, outputid, internal=False):
        """\
        Get the value of an output.

        @param outputid: The output ID.
        @type outputid: C{str}
        """
        if not internal and not outputid in self.outputs:
            raise KeyError('no output %s' % outputid)
        if not internal and len(self._outputs):
            return self.get_output(self._outputs[outputid], internal=True)
        else:
            deviceid = outputid.split('.')[0]
            outputid = '.'.join(outputid.split('.')[1:])
            return self._devices[deviceid].get_output(outputid)

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
                if self.get_output('%s.%s' % cached_output, internal=True) != \
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
