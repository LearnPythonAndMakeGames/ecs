#!/usr/bin/env python
import sys

from ecs import Entity
from components import Health, Damage

if sys.platform.startswith('2'):
    range = xrange

def setup_entities(number_of_cowboys=100, number_of_aliens=100):
    '''Sets up all the entities'''

    # Generate entities and add components to them
    cowboys = []
    for cowboy in range(number_of_cowboys):
        cowboy = Entity('cowboy-{:02}'.format(cowboy))
        cowboy.health = Health(cowboy, current=51, max=53)
        cowboy.damage = Damage(cowboy, normal=12, critical=17, critical_percent=19)
        cowboy.humanoid = 'cowboy'
        cowboys.append(cowboy)

    aliens = []
    for alien in range(number_of_aliens):
        alien = Entity('alien-{:02}'.format(alien))
        alien.health = Health(alien, current=102, max=102)
        alien.damage = Damage(alien, normal=6, critical=8, critical_percent=20)
        alien.humanoid = 'alien'
        aliens.append(alien)

    # Convenient dictionary splitting the two types of entities
    entities = {'cowboys': cowboys, 'aliens': aliens}
    return entities


if __name__ == '__main__':
    from doctest import testmod

    testmod()
