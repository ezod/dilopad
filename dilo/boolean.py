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
        @type term: C{str} or L{BooleanExpression}
        @param complement: True if the expression is complemented.
        @type complement: C{bool}
        """
        self.term = term
        self.complemented = complemented

    def __str__(self):
        """\
        String representation.
        """
        string = str(self.term)
        if self.complemented:
            if isinstance(self.term, BooleanSum) \
            or isinstance(self.term, BooleanProduct):
                string = '(' + string + ')'
            string = string + '\''
        return string

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


class BooleanSum(BooleanExpression):
    """\
    Boolean sum class.
    """
    def __init__(self, term, complemented=False):
        """\
        Constructor.

        @param term: The term of the Boolean expression.
        @type term: C{str} or L{BooleanExpression}
        @param complement: True if the expression is complemented.
        @type complement: C{bool}
        """
        super(BooleanSum, self).__init__(term, complemented)

    def __str__(self):
        """\
        String representation.
        """
        return ' + '.join([str(expression) for expression in self.term])

    def evaluate(self, values):
        """\
        Evaluate this boolean sum for a given set of variable values.
        
        @param values: The variable values.
        @type values: C{dict} of C{bool}
        @return: The value of the boolean expression.
        @rtype: C{bool}
        """
        value = False
        for expression in self.term:
            value = value or expression.evaluate(values)
        return self.complemented is not value


class BooleanProduct(BooleanExpression):
    """\
    Boolean product class.
    """
    def __init__(self, term, complemented=False):
        """\
        Constructor.

        @param term: The term of the Boolean expression.
        @type term: C{str} or L{BooleanExpression}
        @param complement: True if the expression is complemented.
        @type complement: C{bool}
        """
        super(BooleanProduct, self).__init__(term, complemented)

    def __str__(self):
        """\
        String representation.
        """
        strings = []
        for expression in self.term:
            if isinstance(expression, BooleanSum):
                strings.append('(' + str(expression) + ')')
            else:
                strings.append(str(expression))
        return ' * '.join(strings)

    def evaluate(self, values):
        """\
        Evaluate this boolean product for a given set of variable values.
        
        @param values: The variable values.
        @type values: C{dict} of C{bool}
        @return: The value of the boolean expression.
        @rtype: C{bool}
        """
        value = True
        for expression in self.term:
            value = value and expression.evaluate(values)
        return self.complemented is not value
