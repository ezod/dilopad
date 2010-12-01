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

from re import sub
from pyparsing import Word, alphas, oneOf, operatorPrecedence, opAssoc


class BooleanExpression(object):
    """\
    Boolean expression class.
    """
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, values):
        class BooleanOperator(object):
            def __init__(self, t):
                self.args = t[0][0::2]
            def __str__(self):
                sep = ' %s ' % self.symbol
                return '(' + sep.join(map(str, self.args)) + ')'

        class BooleanAnd(BooleanOperator):
            symbol = '*'
            def __nonzero__(self):
                for a in self.args:
                    if isinstance(a, basestring):
                        v = values[a]
                    else:
                        v = bool(a)
                    if not v:
                        return False
                return True

        class BooleanOr(BooleanOperator):
            symbol = '+'
            def __nonzero__(self):
                for a in self.args:
                    if isinstance(a, basestring):
                        v = values[a]
                    else:
                        v = bool(a)
                    if v:
                        return True
                return False

        class BooleanNot(BooleanOperator):
            def __init__(self, t):
                self.arg = t[0][0]
            def __str__(self):
                return str(self.arg) + '\''
            def __nonzero__(self):
                if isinstance(self.arg, basestring):
                    v = values[self.arg]
                else:
                    v = bool(self.arg)
                return not v

        BooleanOperand = Word(alphas, max=1) | oneOf('1 0')

        BooleanAlgebra = operatorPrecedence(BooleanOperand,
            [('!', 1, opAssoc.LEFT, BooleanNot),
             ('*', 2, opAssoc.LEFT, BooleanAnd),
             ('+', 2, opAssoc.LEFT, BooleanOr)])

        res = BooleanAlgebra.parseString(sub('\'', '!', self.expression))[0]
        return bool(res)
