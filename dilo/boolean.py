  #   #               #
  #   #               #
### # # ### ### ### ###
# # # # # # # # # # # #
### # # ### ###  ## ###
            #
            #

"""\
Boolean algebra module.

@author: Aaron Mavrinac
@contact: mavrinac@gmail.com
@license: GPL-3
"""

class BooleanVariable(tuple):
    """\
    Boolean variable class.
    """
    def __new__(cls, iterable):
        """\
        Constructor.
        """
        return tuple.__new__(cls, iterable)

    def __str__(self):
        """\
        String representation.
        """
        if self[1]:
            return self[0]
        else:
            return self[0] + '\''

    def evaluate(self, values):
        """\
        Evaluate this boolean sum for a given set of variable values.
        
        @param values: The variable values.
        @type values: C{dict} of C{bool}
        @return: The value of the boolean expression.
        @rtype: C{bool}
        """
        try:
            if self[1]:
                return values[self[0]]
            else:
                return not values[self[0]]
        except KeyError:
            raise KeyError('missing variable value')


class BooleanSum(tuple):
    """\
    Boolean sum class.
    """
    def __new__(cls, iterable):
        """\
        Constructor.
        """
        return tuple.__new__(cls, iterable)
    
    def __str__(self):
        """\
        String representation.
        """
        return '(' + ' + '.join([str(expression) for expression in self]) + ')'

    def evaluate(self, values):
        """\
        Evaluate this boolean sum for a given set of variable values.
        
        @param values: The variable values.
        @type values: C{dict} of C{bool}
        @return: The value of the boolean expression.
        @rtype: C{bool}
        """
        value = False
        for expression in self:
            value = value or expression.evaluate(values)
        return value


class BooleanProduct(tuple):
    """\
    Boolean product class.
    """
    def __new__(cls, iterable):
        """\
        Constructor.
        """
        return tuple.__new__(cls, iterable)

    def __str__(self):
        """\
        String representation.
        """
        return ' * '.join([str(expression) for expression in self])

    def evaluate(self, values):
        """\
        Evaluate this boolean product for a given set of variable values.
        
        @param values: The variable values.
        @type values: C{dict} of C{bool}
        @return: The value of the boolean expression.
        @rtype: C{bool}
        """
        value = True
        for expression in self:
            value = value and expression.evaluate(values)
        return value
