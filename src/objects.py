import random
import numpy as np
from src import config


############################################################################################################
############################################################################################################
class WorldObject:
    ############################################################################################################
    def __init__(self):
        self.position = [None, None]
        self.object_type = None
        self.graphic_object = None
        self.image = None
        self.appearance = None
        self.quantity = None

    ############################################################################################################
    def next_turn(self):
        pass


############################################################################################################
############################################################################################################
class Carcass(WorldObject):
    ############################################################################################################
    def __init__(self, object_type, image, appearance, size, the_world):
        WorldObject.__init__(self)
        self.object_type = object_type
        self.quantity = 100 * size
        self.appearance = appearance
        self.the_world = the_world
        self.init_appearance()
        self.id_number = the_world.entity_counter
        self.graphic_object = image
        self.decay_rate = config.Carcass.decay_rate

        self.the_world.entity_counter += 1

    ############################################################################################################
    def init_appearance(self):
        if len(self.appearance) < 10:
            num_dead_bits = 3
        else:
            num_dead_bits = 5

        for i in range(num_dead_bits):
            self.appearance[-i] = 0.5

    ############################################################################################################
    def next_turn(self):
        self.quantity -= self.decay_rate
        if self.quantity <= 0:
            self.the_world.map[tuple(self.position)].object_list.remove(self)
            self.the_world.object_list.remove(self)
            self.the_world.object_counts_dict[self.object_type] -= 1



