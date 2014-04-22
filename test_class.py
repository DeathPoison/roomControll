#!/usr/bin/env python


class a():
    def __init__(self):
        self.abc = 'xy'

b = a()         # create instance
print b.abc     # class variable

var = raw_input('var:')
val = raw_input('val:')

b.__dict__[var] = val

# print b.var
print b.abc
