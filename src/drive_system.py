from src import config
import numpy as np


############################################################################################################
############################################################################################################
class DriveSystem:
    ############################################################################################################
    def __init__(self, animal):
        self.animal = animal
        self.num_drives = None
        self.drive_list = None
        self.drive_index_dict = None
        self.drive_value_array = None

        self.action_drive_change_dict = config.Animal.action_drive_change_dict

        self.init_drives()

    ############################################################################################################
    def __repr__(self):
        output_string = "Drive System: {} Drives\n".format(self.num_drives)
        for i in range(self.num_drives):
            output_string += "    {:8s}: {:0.4f}\n".format(self.drive_list[i], self.drive_value_array[i])
        return output_string

    ############################################################################################################
    def init_drives(self):

        for action in self.action_drive_change_dict:
            self.num_drives = 0
            self.drive_list = []
            self.drive_index_dict = {}
            for drive in self.action_drive_change_dict[action]:
                self.drive_list.append(drive)
                self.drive_index_dict[drive] = self.num_drives
                self.num_drives += 1

        self.drive_value_array = np.ones([self.num_drives], float) * 0.05

    ############################################################################################################
    def update_drives(self, action_choice):

        # the action taken, so we can enact its effects
        action_effect_dict = self.action_drive_change_dict[action_choice]

        # update the drives
        for i in range(self.num_drives):
            drive = self.drive_list[i]

            if drive == 'Energy':
                # metabolism and size effect how much energy things take
                self.drive_value_array[i] += (self.animal.current_size * action_effect_dict[drive]
                                              * self.animal.metabolism)/100
            else:
                self.drive_value_array[i] += action_effect_dict[drive]/100

        # drop health by the starvation rate
        if self.drive_value_array[self.drive_index_dict['Energy']] <= 0:
            self.drive_value_array[self.drive_index_dict['Health']] -= config.Animal.starvation_rate/100

        # cap all drives between 0 and 1
        for i in range(self.num_drives):
            if self.drive_value_array[i] < 0:
                self.drive_value_array[i] = 0
            if self.drive_value_array[i] > 1:
                self.drive_value_array[i] = 1