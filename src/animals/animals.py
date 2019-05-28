import random
import numpy as np
from src import config
from src.animals import phenotype, drive_system, nervous_system, action_system, genome


class Animal:
    ############################################################################################################
    def __init__(self, the_world, mother_genome, father_genome):
        ############################################################################################################
        self.the_world = the_world  # a reference to the world data structure
        self.kingdom = "Animal"  # this animal's kingdom type (ie plant or animal)
        self.species = None  # this animal's species type
        self.graphic_object = None  # this animal's graphic object, currently a python turtle object
        self.dead_graphic_object = None
        self.id_number = the_world.entity_counter  # a unique id number
        self.the_world.entity_counter += 1

        ############################################################################################################
        self.appearance = None
        self.age = 0
        self.current_size = 0.1  # the animal's current size, global range 0-5, actual range specified genetically
        self.position = None    # the animal's coordinates
        self.orientation = random.choice([0, 90, 180, 270])  # can make this nonrandom later
        self.pregnant = 0
        self.baby_daddy_genome = None
        self.fetus = None

        ############################################################################################################
        self.attack_strength = config.Animal.attack_strength  # the force modifier this animal gets when attacking\
        self.species_metabolism_multiplier = 1
        self.metabolism = config.Animal.metabolism * self.species_metabolism_multiplier
        self.allowed_terrain_dict = config.Animal.allowed_terrain_dict
        self.action_drive_change_dict = config.Animal.action_drive_change_dict
        self.diet_dict = None

        ############################################################################################################
        self.genome = genome.Genome(self, mother_genome, father_genome)
        self.phenotype = phenotype.Phenotype(self)
        self.drive_system = drive_system.DriveSystem(self)
        self.action_system = action_system.ActionSystem(self)
        self.nervous_system = nervous_system.NervousSystem(self)
        self.update_appearance()

    ############################################################################################################
    def __repr__(self):
        output_string = "{} {}\n".format(self.species, self.id_number)
        output_string += "    Position:     {}\n".format(self.position)
        output_string += "    Orientation:  {}\n".format(self.orientation)
        output_string += "    Age:          {}\n".format(self.age)
        output_string += "    Current Size: {}\n".format(self.current_size)
        output_string += "    Sex:          {}\n".format(self.phenotype.trait_value_dict['Sex'])
        output_string += "    Pregnant:     {}\n".format(self.pregnant)
        return output_string

    ############################################################################################################
    def take_turn(self):
        self.nervous_system.stored_neural_feedforward()
        self.action_system.action_turn()
        self.drive_system.update_drives(self.action_system.action_choice)
        self.nervous_system.update_sensory_state()
        self.nervous_system.update_neural_weights()
        self.grow_older()
        self.update_appearance()

    ############################################################################################################
    def grow_older(self):
        self.age += 1

        if self.current_size < self.phenotype.trait_value_dict['Max Size']:
            self.current_size += 1/config.Animal.childhood_length
            if self.current_size > self.phenotype.trait_value_dict['Max Size']:
                self.current_size = self.phenotype.trait_value_dict['Max Size']

    ############################################################################################################
    def get_pregnant(self, father_genome):
        self.pregnant = 1
        self.baby_daddy_genome = father_genome
        self.metabolism = config.Animal.metabolism * self.species_metabolism_multiplier * \
                          config.Animal.pregnant_metabolism_multiplier

    ############################################################################################################
    def bear_child(self):
        self.fetus.current_size = 0.1
        self.fetus.appearance[0] = self.fetus.current_size / 5
        self.fetus.age = 0
        self.pregnant = 0
        self.fetus = None
        self.metabolism = config.Animal.metabolism * self.species_metabolism_multiplier

    ############################################################################################################
    def update_appearance(self, appearance=None):
        if appearance is not None:
            current_appearance = np.zeros([len(appearance)], float)

            for i in range(len(appearance)):
                if random.random() < config.Animal.appearance_variance:
                    if appearance[i] == 0:
                        current_appearance[i] = 1
                    else:
                        current_appearance[i] = 0
                else:
                    current_appearance[i] = appearance[i]

            self.genome.gene_list[self.genome.gene_index_dict['Appearance']] = np.copy(current_appearance).astype(int)
            self.phenotype.trait_value_dict['Appearance'] = current_appearance

        self.appearance = self.phenotype.trait_value_dict['Appearance']
        self.appearance[0] = self.current_size / 5