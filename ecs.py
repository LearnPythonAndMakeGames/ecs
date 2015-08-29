#!/usr/bin/env python
'''
Entity Component System for Python

ecs.py provides a convenient library to utilize for the ECS pattern.

'''
from collections import OrderedDict as dict
import json
from uuid import uuid4
import sys

__version__ = '0.1.3'
__license__ = 'Apache 2.0'
__url__ = 'http://learnpythonandmakegames.github.io/ecs/'
__author__ = 'Learn Python and Make Games'


class Entity(object):
    '''More or less a container for an id.

    Entities have a relationship to their components.

    >>> e = Entity('player', 0)
    >>> e
    <Entity player:0>
    >>> print e
    {}
    >>> e.heart = 1
    >>> print e
    {'heart': 1}
    >>> print e['heart']
    1
    >>> print e.components
    {'heart': 1}
    >>> Health = ComponentFactory('Health', current=100, max=100)
    >>> Mana = ComponentFactory('Mana', current=100, max=100)
    >>> e.health = Health(current=98)
    >>> e.mana = Mana(current=64)
    >>> print(e.components)
    {'heart': 1, 'health': <Health entity:player.health>, 'mana': <Mana entity:player.mana>}
    '''
    Catalog = {}

    __slots__ = ('uid', 'name', 'components')

    def __new__(cls, name=None, uid=None):
        '''We only want one entity with the same name

        >>> player1 = Entity('player1')
        >>> player2 = Entity('player2')
        >>> player3 = Entity('player1')
        >>> player1 == player2
        False
        >>> player1 == player3
        True
        '''
        if name not in cls.Catalog:
            entity = super(Entity, cls).__new__(cls)
            cls.Catalog[name] = entity
        else:
            entity = cls.Catalog[name]
        return entity

    def __hash__(self):
        return hash(self.uid)

    def __init__(self, name=None, uid=None):
        self.uid = uuid4() if uid is None else uid
        self.name = name or ''
        self.components = {}

    def __repr__(self):
        cname = self.__class__.__name__
        name = self.name or self.uid
        if name != self.uid:
            name = '{}:{}'.format(name, self.uid)
        return "<{} {}>".format(cname, name)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.uid == other.uid
        elif isinstance(other, self.uid.__class__):
            return self.uid == other
        return False

    def __str__(self):
        return str(self.components)

    def __getitem__(self, key):
        '''Allows access to entity components and their properties.
        '''
        return self.components[key]

    def __setitem__(self, key, value):
        '''Allows modification to components.
        '''
        if isinstance(value, Component):
            value.entity = self
        self.Catalog[key] = value

    def __getattr__(self, key, *args, **kwds):
        '''Allows access to properties as an attribute:
        '''
        if key in super(Entity, self).__getattribute__('__slots__'):
            return super(Entity, self).__getattr__(key)
        else:
            return self.components[key]

    def __setattr__(self, key, value):
        '''Allows modification to properties as an attribute:
        '''
        if key in super(Entity, self).__getattribute__('__slots__'):
            super(Entity, self).__setattr__(key, value)
        else:
            # Create relationships between the entity and components
            if isinstance(value, Component):
                vCatalog = value.__class__.Catalog
                if value.entity is None:
                    value.entity = self
                    # Update the component catalog with the entry
                    for entity, comp in vCatalog.items():
                        if comp == value:
                            if entity in vCatalog:
                                vCatalog.pop(entity)
                            vCatalog[self] = value
            # Even if it is not technically a component, still add it
            #  as a simple 'attribute' component.
            self.components[key] = value

    def __del__(self):
        '''Remove the relationship from all component data'''
        for attr, component in self.components.items():
            if hasattr(component, 'entity'):
                component.entity = None
                component.__class__.Catalog.pop(self)
        self.__class__.Catalog.pop(self.name)


class Component(object):
    '''Contains a set of unique properties

    Components have a tightly coupled relationship with an entity

    >>> HealthComponent = ComponentFactory('Health', current=100, max=100)
    >>> player = Entity('Player')
    >>> player.health = HealthComponent(current=10)
    >>> player.health
    <Health entity:Player.health>
    >>> print(player.health)
    {
        "current": 10,
        "max": 100
    }
    >>> player.health.current
    10
    >>> isinstance(player.health, Component)
    True
    >>> isinstance(player.health, HealthComponent)
    True
    '''

    __slots__ = ('entity')
    defaults = {}
    Catalog = {}
    ComponentTypes = {}

    def __new__(cls, entity=None, **properties):
        cname = cls.__name__
        if cname not in Component.ComponentTypes:
            Component.ComponentTypes[cname] = cls
            cls.Catalog = {}
        if entity is not None:
            if entity not in cls.Catalog:
                component = super(Component, cls).__new__(cls)
                cls.Catalog[entity] = component
            else:
                component = cls.Catalog[entity]
        else:
            component = super(Component, cls).__new__(cls)
        return component

    def __hash__(self):
        return (hash(self.Catalog) ^
                hash(self.ComponentTypes) ^
                hash(self.defaults) ^
                hash(self.entity) ^
                hash(self))

    def __init__(self, entity=None, **properties):
        self.entity = entity
        for prop, val in self.defaults.items():
            setattr(self, prop, properties.get(prop, val))

    def get(self, key, default):
        '''Provides a way to look up a key without creating an exception
        if the key is not found, default is returned.
        '''

    def reset(self):
        '''Returns component to default state'''
        for prop, val in self.defaults.items():
            setattr(self, prop, val)

    def __iter__(self):
        '''Iterates over property names
        '''
        for prop in self.defaults:
            yield prop

    def __getitem__(self, key):
        '''Makes it possible to access attributes as an index'''
        return getattr(self, key)

    def __setitem__(self, key, value):
        '''Makes it possible to modify attributes as an index'''
        setattr(self, key, value)

    def __repr__(self):
        '''Just show the minimum needed
        '''
        cname = self.__class__.__name__
        title = ''
        if self.entity:
            for prop_name, component in self.entity.components.items():
                if component == self:
                    title = ' entity:{}.{}'.format(self.entity.name, prop_name)
                    break
        return '<{}{}>'.format(cname, title)

    def __str__(self):
        '''Just dump the json of the properties
        '''
        keys = self.defaults.keys()
        data = dict()
        for key in keys:
            if key != 'defaults':
                data[key] = getattr(self, key, self.defaults.get(key))
        json_string = '\n'.join(
            line.rstrip()
            for line in json.dumps(data, indent=4).split('\n')
            )
        return json_string

    def __del__(self):
        '''Remove the relationship from the entity'''
        if self.entity:
            for attr, component in self.entity.components.items():
                if component == self:
                    self.entity.components.pop(attr)
                    break
        if self.entity in self.__class__.Catalog:
            self.__class__.Catalog.pop(self.entity)


class ComponentFactory(object):
    '''Factory for Component classes

    >>> HealthComponent = ComponentFactory('Health', current=100, max=100)
    >>> HealthComponent
    <class '__main__.Health'>
    '''
    Catalog = {}

    __slots__ = ()

    def __new__(cls, title, **attributes):
        '''Ties name of component to a specific instance, which is shared by
        all components of the same template'''
        # new_class = type(type_name, type_class_bases, type_attributes)
        defaults = dict((k, v) for k, v in attributes.items())
        if title not in cls.Catalog:
            Component.ComponentTypes[title] = cls
            template_cls = type(title, (Component, ), attributes)
            template_cls.Catalog = {}
            template_cls.defaults = defaults
            cls.Catalog[title] = template_cls
        else:
            template_cls = cls.Catalog[title]
            for attr in attributes:
                if not hasattr(template_cls, attr):
                    msg = 'Component attribute mismatch: {} vs {}'
                    msg = msg.format(attributes, template_cls.defaults)
                    raise RuntimeError(msg)
        return template_cls


class System(object):
    '''Identifies a set of components that need to be grouped for tasks

    Systems have a loose coupling with Components and Entities through
    the ComponentFactory Catalog.

    # Initialize entities and their components
    >>> player = Entity('player', 1)
    >>> skeleton = Entity('skeleton', 2)
    >>> Position = ComponentFactory('Position', x=0, y=0)
    >>> Velocity = ComponentFactory('Velocity', angle=0, speed=0)
    >>> player.position = Position(x=10, y=10)
    >>> player.velocity = Velocity(angle=270, speed=1)
    >>> skeleton.position = Position(x=0, y=5)
    >>> skeleton.velocity = Velocity(angle=45, speed=1)

    >>> print player
    {'position': <Position entity:player.position>, 'velocity': <Velocity entity:player.velocity>}
    >>> print skeleton
    {'position': <Position entity:skeleton.position>, 'velocity': <Velocity entity:skeleton.velocity>}

    >>> MovementSystem = System('Movement', positions=Position, velocity=Velocity)
    >>> MovementSystem
    <System Movement>
    >>> MovementSystem.update()
    Traceback (most recent call last):
    ...
    NotImplementedError: Abstract method
    >>> sorted(MovementSystem.entities)
    [<Entity player:1>, <Entity skeleton:2>]
    >>> sorted(MovementSystem.components)
    [<Position entity:player.position>, <Position entity:skeleton.position>, <Velocity entity:player.velocity>, <Velocity entity:skeleton.velocity>]
    '''
    components = []
    Catalog = {}

    __slots__ = ()

    def __new__(cls, name=None, components=[]):
        name = cls.__name__ if name is None else name
        if name not in System.Catalog:
            system = super(System, cls).__new__(cls)
            System.Catalog[name] = system
        else:
            system = System.Catalog[name]
        return system

    def __init__(self, name=None, components=[]):
        self.name = name
        if components:
            self.components = components

    @property
    def entities(self):
        return list(set(entity
                        for component_cls in self.component_classes
                        for entity in component_cls.Catalog.keys()
                        if entity is not None))


    @property
    def component_classes(self):
        return list(set(Component.ComponentTypes.get(component_name)
                        for component_name in self.components
                        if component_name in Component.ComponentTypes
                        ))

    def get_components(self):
        '''Creates a dictionary of component classes'''

    def update(self, dt=None):
        '''Runs an update on the various components'''
        raise NotImplementedError('Abstract method')

    def __repr__(self):
        cname = self.__class__.__name__
        name = self.name
        return '<{} {}>'.format(cname, name)

if __name__ == '__main__':
    from doctest import testmod

    testmod()
