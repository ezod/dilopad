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

class BooleanExpression(object):
    """\
    Boolean expression class.
    """
    def __init__(self, term, complemented=False):
        """\
        Constructor.

        @param term: The term of the Boolean expression.
        @type term: C{str} or L{BooleanSum} or L{BooleanProduct}
        @param complement: True if the expression is complemented.
        @type complement: C{bool}
        """
        self.term = term
        self.complemented = complemented

    def __str__(self):
        """\
        String representation.
        """
        if self.complemented:
            return str(self.term) + '\''
        else:
            return str(self.term)

    def evaluate(self, values):
        """
        Evaluate this Boolean expression for a given set of variable values.
        
        @param values: The variable values.
        @type values: C{dict} of C{bool}
        @return: The value of the boolean expression.
        @rtype: C{bool}
        """
        try:
            return self.complemented is not self.term.evaluate(values)
        except AttributeError:
            try:
                return self.complemented is not values[self.term]
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
        return '(' + ' * '.join([str(expression) for expression in self]) + ')'

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
