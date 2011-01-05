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
    def __init__(self, pos=(0, 0)):
        """\
        Constructor. Not to be instantiated directly.

        @param pos: The position of this device.
        @type pos: C{tuple} of C{int}
        """
        self.pos = pos
        self._inputs = {}
        self._outputs = {}
        if self.__class__ is Device:
            raise NotImplementedError('cannot instantiate an abstract device')

    @property
    def inputs(self):
        """\
        A list of inputs to this device.
        """
        inputs = list(self._inputs.keys())
        inputs.sort()
        return inputs

    @property
    def outputs(self):
        """\
        A list of outputs from this device.
        """
        outputs = list(self._outputs.keys())
        outputs.sort()
        return outputs

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

    def draw(self, cr):
        """\
        Draw this device.

        @param cr: The Cairo context resource.
        @type cr: L{cairo_context}
        """
        raise NotImplementedError('draw method must be overridden')


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
            if not (deviceid, inputid) in self._connections]
    
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
            inputs = list(self._inputs.keys())
        else:
            inputs = self._internal_inputs()
        inputs.sort()
        return inputs

    @property
    def outputs(self):
        """\
        A list of outputs from this circuit. By default, the set of outputs is
        generated as all outputs of the circuit's devices.
        """
        if len(self._outputs):
            outputs = list(self._outputs.keys())
        else:
            outputs = self._internal_outputs()
        outputs.sort()
        return outputs

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
        if deviceid in self._devices:
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
        connections = list(self._connections.keys())
        for connection in connections:
            if connection[0] == deviceid:
                del self._connections[connection]
            elif self._connections[connection][0] == deviceid:
                del self._connections[connection]
        # delete cached outputs
        cached_outputs = list(self._cached_outputs.keys())
        for cached_output in cached_outputs:
            if cached_output[0] == deviceid:
                del self._cached_outputs[cached_output]
        # delete labels
        for inputid in self._devices[deviceid].inputs:
            labels = list(self._inputs.keys())
            for label in labels:
                self._inputs[label].discard('%s.%s' % (deviceid, inputid))
                if not len(self._inputs[label]):
                    del self._inputs[label]
        for outputid in self._devices[deviceid].outputs:
            labels = list(self._outputs.keys())
            for label in labels:
                if self._outputs[label] == '%s.%s' % (deviceid, outputid):
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

    def draw(self, cr):
        """\
        Draw this circuit (all contained devices and connections).

        @param cr: The Cairo context resource.
        @type cr: L{cairo_context}
        """
        for deviceid in self._devices.keys():
            self._devices[deviceid].draw(cr)
        # TODO: draw connections
