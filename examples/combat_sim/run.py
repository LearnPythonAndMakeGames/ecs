#!/usr/bin/env python
'''
Description:
    Runs a combat simulator -- Cowboys vs Aliens

Usage: run [options] [--memory | --compute]

Options:
    -c --cowboys NUMBER    Number of cowboys [default: 10]
    -a --aliens NUMBER     Number of aliens [default: 10]
    -q --quiet             Reduces verbosity
    -m --memory            Profiles memory
    -x --compute           Profiles execution time
'''
from entities import setup_entities
from systems import CombatSystem

def simulate(number_of_cowboys, number_of_aliens, quiet=False):
    '''Simulates combat between aliens and cowboys'''
    combat_system = CombatSystem()

    entities = setup_entities(number_of_cowboys, number_of_aliens)

    combat_round = 0
    print('='*40)
    print(' Combat Sim: Cowboys vs Aliens')
    print('-'*40)
    if not quiet:
        print("Round: # -- C | A")
        print('-----------------')
    while True:
        cowboys_alive = sum(e.health.alive for e in entities['cowboys'])
        aliens_alive = sum(e.health.alive for e in entities['aliens'])
        if cowboys_alive == 0 or aliens_alive == 0:
            break
        if not quiet:
            results = "Round: {} -- {} | {}"
            print(results.format(combat_round, cowboys_alive, aliens_alive))
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
    print('\n')


def handle_cli():
    from docopt import docopt

    args = docopt(__doc__)

    kwds = {
        'number_of_cowboys': int(args.get('--cowboys')),
        'number_of_aliens': int(args.get('--aliens')),
        'quiet': args.get('--quiet', None),
        'memory': args.get('--memory', None),
        'compute': args.get('--compute', None)
    }

    return kwds

if __name__ == '__main__':
    kwds = handle_cli()
    use_memory_profiler = kwds.pop('memory')
    use_compute_profiler = kwds.pop('compute')

    # Adds a method for benchmarking memory
    if use_memory_profiler:
        from memory_profiler import profile
        # Hack for on-demand decoration
        simulate = profile()(simulate)
        simulate(**kwds)

    # Adds a method for benchmarking compute
    elif use_compute_profiler:
        import cProfile as profile
        import os
        import pstats
        import sys

        cmd = 'simulate({number_of_cowboys}, {number_of_aliens}, {quiet})'
        cmd = cmd.format(**kwds)
        if not os.path.exists('benchmarks'):
            os.mkdir('benchmarks')
        version = sys.version.split(' ')[0]
        fname = 'benchmarks/compute.{}.bin'.format(str(version))
        profile.run(cmd, fname)

        p = pstats.Stats(fname)
        p.strip_dirs().sort_stats('cumulative').print_stats(10)

    # Otherwise just run it
    else:
        simulate(**kwds)

