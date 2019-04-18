from src import config
from src import animals
from src import plants
from src import terrain
import random
import sys
import numpy as np


############################################################################################################
############################################################################################################
class World:

    def __init__(self):

        self.current_turn = 0
        self.entity_counter = 0

        self.world_size = 0
        self.land_size = 0
        self.water_size = 0
        self.num_rows = config.World.rows
        self.num_columns = config.World.columns
        self.map = {}

        self.animal_list = []
        self.plant_list = []
        self.object_list = []
        self.dead_animal_list = []
        self.plant_species_counts_dict = {}
        self.animal_species_counts_dict = {}
        self.object_counts_dict = {}

        self.turn_summary_dict = None
        self.initial_animal_summary_dict = None

        self.appearance_dict = None
        random_seed = config.GlobalOptions.random_seed
        if random_seed is None:
            self.random_seed = random.randint(0, 32768)
        else:
            self.random_seed = config.GlobalOptions.random_seed

        random.seed(self.random_seed)
        np.random.seed(self.random_seed)

        self.generate_appearances()
        self.generate_world()
        self.generate_plants()
        self.generate_animals()
        self.generate_objects()
        self.calc_turn_summary()
        self.calc_initial_animal_summaries()

        if config.Animal.output_data:
            self.animal_summary_filename = "output/" + str(self.random_seed) + "_animals_n" + str(len(self.animal_list)) + ".txt"

    ############################################################################################################
    def generate_appearances(self):
        self.appearance_dict = {}

        for terrain_type in ['Lake', 'Plains', 'Desert']:
            self.appearance_dict[terrain_type] = np.random.randint(0, 2, [config.World.appearance_size]).astype(float)

        for species in ['Grass']:
            self.appearance_dict[species] = np.random.randint(0, 2, [config.World.appearance_size]).astype(float)

        for species in ['Lion', 'Zebra']:
            self.appearance_dict[species] = np.random.randint(0, 2, [config.World.appearance_size]).astype(float)

    ############################################################################################################
    def generate_world(self):
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                self.world_size += 1
                new_tile = self.choose_tile_type(i, j)
                self.map[(j, i)] = new_tile
        self.land_size = self.world_size - self.water_size

    ############################################################################################################
    def choose_tile_type(self, i, j):
        if (i == 0) or (i == self.num_rows - 1) or (j == 0) or (j == self.num_columns - 1):
            new_tile = terrain.Lake(j, i)
            new_tile.change_appearance(self.appearance_dict['Lake'])
            self.water_size += 1
        else:
            lake_value = random.uniform(0, 1)
            if lake_value < config.Terrain.lake_prob:
                new_tile = terrain.Lake(j, i)
                new_tile.change_appearance(self.appearance_dict['Lake'])
                self.water_size += 1
            else:
                plains_value = random.uniform(0, 1)
                if plains_value < config.Terrain.plains_prob:
                    new_tile = terrain.Plains(j, i)
                    new_tile.change_appearance(self.appearance_dict['Plains'])
                else:
                    new_tile = terrain.Desert(j, i)
                    new_tile.change_appearance(self.appearance_dict['Desert'])

        return new_tile

    ############################################################################################################
    def generate_plants(self):

        for i in range(self.num_rows):
            for j in range(self.num_columns):
                if self.map[(j, i)].terrain_type == 'Plains':
                    new_grass = plants.Grass(self)
                    new_grass.change_appearance(self.appearance_dict['Grass'])
                    self.map[(j, i)].plant_list.append(new_grass)
                    self.plant_list.append(new_grass)

                    if 'Grass' not in self.plant_species_counts_dict:
                        self.plant_species_counts_dict['Grass'] = 1
                    else:
                        self.plant_species_counts_dict['Grass'] += 1

    ############################################################################################################
    def generate_animals(self):

        for i in range(config.Lion.start_number):
            self.animal_list.append(animals.Lion(self, None, None))

        for i in range(config.Zebra.start_number):
            self.animal_list.append(animals.Zebra(self, None, None))

        if len(self.animal_list) > self.land_size:
            print("ERROR: Number of animals is > the number of land tiles")
            sys.exit(2)
        else:
            random.shuffle(self.animal_list)

            for i in range(len(self.animal_list)):
                self.animal_list[i].update_appearance(self.appearance_dict[self.animal_list[i].species])

                if self.animal_list[i].species not in self.animal_species_counts_dict:
                    self.animal_species_counts_dict[self.animal_list[i].species] = 1
                else:
                    self.animal_species_counts_dict[self.animal_list[i].species] += 1

                self.place_animal(self.animal_list[i])

    ############################################################################################################
    def place_animal(self, animal, position=None):
        if position is None:
            placed = False
            while not placed:
                column = random.randint(0, config.World.columns - 1)
                row = random.randint(0, config.World.rows - 1)
                current_tile = self.map[(column, row)]
                terrain_type = current_tile.terrain_type
                if animal.allowed_terrain_dict[terrain_type]:
                    if len(self.map[(column, row)].animal_list) == 0:
                        placed = True
                        animal.position = [column, row]
                        self.map[(column, row)].animal_list.append(animal)
        else:
            animal.position = [position[0], position[1]]
            self.map[(position[0], position[1])].animal_list.append(animal)

    ############################################################################################################
    def generate_objects(self):
        # entity_counter += 1
        pass

    ############################################################################################################
    def calc_turn_summary(self):
        self.turn_summary_dict = {'Plant': {}, 'Animal': {}, 'Object': {}}

        for species in self.plant_species_counts_dict:
            self.turn_summary_dict['Plant'][species] = [self.plant_species_counts_dict[species], 0]
            for plant in self.plant_list:
                self.turn_summary_dict['Plant'][plant.species][1] += plant.quantity

        for species in self.animal_species_counts_dict:
            self.turn_summary_dict['Animal'][species] = [self.animal_species_counts_dict[species], 0, 0, 0]
            for animal in self.animal_list:
                self.turn_summary_dict['Animal'][animal.species][1] += animal.drive_system.drive_value_array[0]
                self.turn_summary_dict['Animal'][animal.species][2] += animal.drive_system.drive_value_array[1]
                self.turn_summary_dict['Animal'][animal.species][3] += animal.drive_system.drive_value_array[2]

            if self.turn_summary_dict['Animal'][species][0]:
                self.turn_summary_dict['Animal'][species][1] /= self.turn_summary_dict['Animal'][species][0]
                self.turn_summary_dict['Animal'][species][2] /= self.turn_summary_dict['Animal'][species][0]
                self.turn_summary_dict['Animal'][species][3] /= self.turn_summary_dict['Animal'][species][0]

    ############################################################################################################
    def calc_initial_animal_summaries(self):
        self.initial_animal_summary_dict = {}
        for species in self.animal_species_counts_dict:
            animal_summary_dict = self.calc_species_summary(species)
            self.initial_animal_summary_dict[species] = animal_summary_dict

    ############################################################################################################
    def calc_species_summary(self, species):

        animal_summary_dict = {'N': self.turn_summary_dict['Animal'][species][0],
                               'Drive Values': self.turn_summary_dict['Animal'][species][1:]}
        sex_sum = 0.0
        age_sum = 0.0
        size_sum = 0.0
        hidden_sum = 0.0
        learning_rate_sum = 0.0
        drive_direction_sums = np.zeros([3], float)
        drive_reinforcement_sums = np.zeros([4, 3], float)
        action_output_sums = np.zeros([6], float)

        for animal in self.animal_list:
            if animal.species == species:
                animal.nervous_system.get_sensory_representation()
                animal.nervous_system.neural_feedforward()

                if animal.phenotype.trait_value_dict['Sex'] == 1:
                    sex_sum += 1
                age_sum += animal.age
                size_sum += animal.phenotype.trait_value_dict['Max Size']
                hidden_sum += animal.phenotype.trait_value_dict['Num Hidden Neurons']
                learning_rate_sum += animal.phenotype.trait_value_dict['Prediction Learning Rate']

                drive_direction_sums += animal.nervous_system.drive_direction_array
                drive_reinforcement_sums += animal.nervous_system.drive_reinforcement_rate_matrix

                action_output_sums += animal.nervous_system.action_outputs

        if animal_summary_dict['N'] > 0:
            animal_summary_dict['Sex'] = sex_sum / animal_summary_dict['N']
            animal_summary_dict['Age'] = age_sum / animal_summary_dict['N']
            animal_summary_dict['Size'] = size_sum / animal_summary_dict['N']
            animal_summary_dict['Hidden Neurons'] = hidden_sum / animal_summary_dict['N']
            animal_summary_dict['Prediction Learning Rate'] = learning_rate_sum / animal_summary_dict['N']
            animal_summary_dict['Drive Direction Values'] = drive_direction_sums / animal_summary_dict['N']
            animal_summary_dict['Drive Reinforcement Rates'] = \
                drive_reinforcement_sums / animal_summary_dict['N']
            animal_summary_dict['Action Outputs'] = action_output_sums / animal_summary_dict['N']
        else:
            animal_summary_dict['Sex'] = sex_sum
            animal_summary_dict['Age'] = age_sum
            animal_summary_dict['Size'] = size_sum
            animal_summary_dict['Hidden Neurons'] = hidden_sum
            animal_summary_dict['Prediction Learning Rate'] = learning_rate_sum
            animal_summary_dict['Drive Direction Values'] = drive_direction_sums
            animal_summary_dict['Drive Reinforcement Rates'] = drive_reinforcement_sums
            animal_summary_dict['Action Outputs'] = action_output_sums

        return animal_summary_dict

    ############################################################################################################
    def next_turn(self):
        if len(self.animal_list):
            for animal in self.animal_list:
                # normal turn actions
                animal.take_turn()

                # deal with pregnancy related matters
                if animal.pregnant:
                    if animal.pregnant == 1:
                        if animal.species == 'Zebra':
                            animal.fetus = animals.Zebra(self, animal.genome, animal.father_genome)
                        elif animal.species == 'Lion':
                            animal.fetus = animals.Lion(self, animal.genome, animal.father_genome)
                    if animal.pregnant >= config.Animal.gestation_rate:
                        x = animal.position[0]
                        y = animal.position[1]

                        location_list = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
                        random.shuffle(location_list)

                        for location in location_list:
                            if self.legal_offspring_location(animal, location):
                                self.animal_list.append(animal.fetus)
                                self.place_animal(animal.fetus, location)
                                self.animal_species_counts_dict[animal.species] += 1
                                animal.bear_child()
                                break
                    else:
                        animal.pregnant += 1

                # deal with dynamica whose health is 0
                if animal.drive_system.drive_value_array[animal.drive_system.drive_index_dict['Health']] <= 0:
                    self.kill_animal(animal)

        self.calc_turn_summary()

        if config.GlobalOptions.summary_freq:
            if self.current_turn % config.GlobalOptions.summary_freq == 0:
                self.print_summary()
                if config.Animal.output_data:
                    self.write_summary()

        self.current_turn += 1

        print("\nturn {}".format(self.current_turn))
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                print("[{} {}]  ".format(j, i), end='')
            print()
        for animal in self.animal_list:
            print(animal.species, animal.id_number, animal.position, self.map[tuple(animal.position)].animal_list)

    ############################################################################################################
    def print_summary(self):
        output_header = "{:<5s} {:<14s}".format("Turn", "ID")
        output_header += "{:<9s} {:<7s} {:<5s}".format("Sex", "Age", "Size")
        output_header += " {:>3s},{:<3s} {:>4s} |".format("X", "Y", "Dir")
        for i in range(self.animal_list[0].drive_system.num_drives):
            output_header += "  {:<7s}".format(self.animal_list[0].drive_system.drive_list[i])
        output_header += " | "
        for i in range(self.animal_list[0].action_system.num_actions):
            if len(self.animal_list[0].action_system.action_list[i]) > 6:
                output_header += "{:<6s} ".format(self.animal_list[0].action_system.action_list[i][:6])
            else:
                output_header += "{:<6s} ".format(self.animal_list[0].action_system.action_list[i])
        output_header += "{:>9s}".format("Choice")
        output_header += " | {:>6s} {:>6s} {:>6s} {:>6s} {:>9s}".format("SpCost",
                                                                        "DpCost", "ApCost", "PpCost", "DrCost")
        print(output_header)

        for animal in self.animal_list:
            output_string = "{:<5s} {:<14s}".format(str(self.current_turn), animal.species+"-"+str(animal.id_number))

            sex = str(animal.phenotype.trait_value_dict['Sex'])
            if animal.pregnant:
                sex = sex + "+1"
            output_string += "{:<9s} {:<7s} {:<5s}".format(sex, str(animal.age),
                                                           str('{:<1.3f}'.format(animal.current_size)))
            output_string += " {:>3s},{:<3s} {:>4s} |".format(str(animal.position[0]), str(animal.position[1]),
                                                              str(animal.orientation))
            for i in range(animal.drive_system.num_drives):
                trimmed_drive = "{:<5.2f}".format(animal.drive_system.drive_value_array[i])
                output_string += "  {:>7s}".format(str(trimmed_drive))
            output_string += " | "

            for i in range(animal.action_system.num_actions):
                trimmed_action = "{:<3.2f} ".format(animal.action_system.legal_action_prob_distribution[i])
                output_string += "{:<6s} ".format(str(trimmed_action))
            output_string += "{:>9s}".format(animal.action_system.action_choice)
            output_string += " | "
            spv = animal.nervous_system.neural_network_prediction_cost[animal.nervous_system.s_indexes[0]:animal.nervous_system.s_indexes[1]]
            dpv = animal.nervous_system.neural_network_prediction_cost[animal.nervous_system.d_indexes[0]:animal.nervous_system.d_indexes[1]]
            apv = animal.nervous_system.neural_network_prediction_cost[animal.nervous_system.a_indexes[0]:animal.nervous_system.a_indexes[1]]
            aapv = animal.nervous_system.neural_network_prediction_cost[animal.nervous_system.aa_indexes[0]:animal.nervous_system.aa_indexes[1]]

            sp_error = np.absolute(spv).sum()
            dp_error = np.absolute(dpv).sum()
            ap_error = np.absolute(apv).sum()
            aap_error = np.absolute(aapv).sum()

            output_string += '{:>6s} '.format('{:<3.2f}'.format(sp_error/animal.nervous_system.s_size))
            output_string += '{:>6s} '.format('{:<3.2f}'.format(dp_error/animal.nervous_system.d_size))
            output_string += '{:>6s} '.format('{:<3.2f}'.format(ap_error/animal.nervous_system.a_size))
            output_string += '{:>6s} '.format('{:<3.2f}'.format(aap_error/animal.nervous_system.aa_size))

            print(output_string)

    ############################################################################################################
    def write_summary(self):
        pass

    ############################################################################################################
    def kill_animal(self, animal):
        self.dead_animal_list.append(animal)

        self.map[tuple(animal.position)].animal_list.remove(animal)
        self.animal_list.remove(animal)
        self.animal_species_counts_dict[animal.species] -= 1
        animal.position = None

    ############################################################################################################
    def legal_offspring_location(self, animal, location):
        if animal.allowed_terrain_dict[self.map[location].terrain_type]:
            if len(self.map[location].animal_list) == 0:
                return True
            else:
                return False
        else:
            return False
