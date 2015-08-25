#!/usr/bin/env python
from ecs import System


class CombatSystem(System):
    '''Updates Health based on Damage components'''

    components = ['Health', 'Damage']

    def update(self, dt=None):
        cowboys = [e for e in self.entities if e.humanoid == 'cowboy' and e.health.alive]
        aliens = [e for e in self.entities if e.humanoid == 'alien' and e.health.alive]

        # Find a live one!
        for cowboy in cowboys:
            if cowboy.health.alive is True:
                break
            else:
                cowboy = None
        for alien in aliens:
            if alien.health.alive is True:
                break
            else:
                alien = None

        # Combat happens simultaneously and to the death
        if cowboy is not None and alien is not None:
            while cowboy.health.alive and alien.health.alive:
                alien.health.current = alien.health.current - cowboy.damage()
                cowboy.health.current = cowboy.health.current - alien.damage()


if __name__ == '__main__':
    from doctest import testmod

    testmod()
