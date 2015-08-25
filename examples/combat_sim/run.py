#!/usr/bin/env python
from entities import setup_entities
from systems import CombatSystem

combat_system = CombatSystem()

entities = setup_entities(4, 4)

combat_round = 0
print('='*40)
print(' Combat Sim: Cowboys vs Aliens')
print('-'*40)
print("Round: # -- C | A")
print('-----------------')
while True:
    cowboys_alive = sum(e.health.alive for e in entities['cowboys'])
    aliens_alive = sum(e.health.alive for e in entities['aliens'])
    if cowboys_alive == 0 or aliens_alive == 0:
        break
    print("Round: {} -- {} | {}".format(combat_round, cowboys_alive, aliens_alive))
    combat_round += 1
    while combat_system.update() is not None:
        continue

print('='*40)
print(' Finished in {} round(s)'.format(combat_round))
print('-'*40)
alive = {
    'cowboys': sum(e.health.alive for e in entities['cowboys']),
    'aliens': sum(e.health.alive for e in entities['aliens'])
}
print('Cowboys alive: {}'.format(alive['cowboys']))
print('Aliens alive: {}'.format(alive['aliens']))
print('-'*40)
if alive['cowboys'] > 0:
    print(' Cowboys win')
elif alive['aliens'] > 0:
    print(' Aliens win')
else:
    print(' Everyone died!')
