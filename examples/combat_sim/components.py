#!/usr/bin/env python
from collections import OrderedDict as dict
from random import randint

from ecs import Component


class Health(Component):
    '''Simple current and max value

    >>> health = Health(current=10)
    >>> print health.current
    10
    >>> health
    <Health>
    >>> print health
    {
        "current": 10,
        "max": 100
    }
    '''
    defaults = dict([('current', 100), ('max', 100)])

    __slots__ = ('entity', 'Catalog', 'ComponentTypes', 'current', 'max')

    @property
    def alive(self):
        return self.current > 0


class Damage(Component):
    '''Simple damage data for a given entity'''
    defaults = dict([('normal', 10), ('critical', 15), ('critical_percent', 10)])

    __slots__ = ('entity', 'Catalog', 'ComponentTypes', 'normal', 'critical', 'critical_percent')

    def __call__(self):
        '''Returns a damage calc based on properties'''
        crit = randint(0, 99) <= (self.critical_percent - 1)
        damage = self.normal
        if crit:
            damage = self.critical
        return damage


if __name__ == '__main__':
    from doctest import testmod

    testmod()
