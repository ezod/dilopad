  #   #               #
  #   #               #
### # # ### ### ### ###
# # # # # # # # # # # #
### # # ### ###  ## ###
            #
            #

"""\
Truth table and Karnaugh map module.

@author: Aaron Mavrinac
@contact: mavrinac@gmail.com
@license: GPL-3
"""

from copy import copy


def binary_combinations(variables, combination={}):
    variables = copy(variables)
    variable = variables.pop(0)
    for value in [False, True]:
        combination[variable] = value
        if len(variables):
            for subcomb in binary_combinations(variables, combination):
                yield subcomb
        else:
            yield combination
