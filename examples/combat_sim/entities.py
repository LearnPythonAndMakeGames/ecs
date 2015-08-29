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
        cowboy.health = Health(cowboy, current=50, max=50)
        cowboy.damage = Damage(cowboy, normal=10, critical=15, critical_percent=10)
        cowboy.humanoid = 'cowboy'
        cowboys.append(cowboy)

    aliens = []
    for alien in range(number_of_aliens):
        alien = Entity('alien-{:02}'.format(alien))
        alien.health = Health(alien, current=100, max=100)
        alien.damage = Damage(alien, normal=5, critical=10, critical_percent=20)
        alien.humanoid = 'alien'
        aliens.append(alien)

    # Convenient dictionary splitting the two types of entities
    entities = {'cowboys': cowboys, 'aliens': aliens}
    return entities


if __name__ == '__main__':
    from doctest import testmod

    testmod()
