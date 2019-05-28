import tkinter as tk
import os
import sys
from src import config
from src.display import button_canvas, summary_frame, main_frame
import time
import numpy as np


class Display:
    ############################################################################################################
    def __init__(self, the_world):
        self.the_world = the_world
        self.turn = 0
        self.image_dict = None
        self.running = False

        self.num_rows = config.World.num_rows
        self.num_columns = config.World.num_columns
        self.grid_size = config.World.grid_size
        self.world_height = None
        self.world_width = None

        self.root = None
        self.root_height = config.GlobalOptions.window_height
        self.root_width = config.GlobalOptions.window_width

        self.main_frame = None
        self.main_canvas = None
        self.main_canvas_height = self.root_height - 50
        self.main_canvas_width = self.root_width - 500 - 15

        self.summary_frame = None
        self.summary_canvas_height = self.root_height - 35
        self.summary_canvas_width = 500

        self.species_summary_window = None

        self.tile_info_window = None
        self.tile_info_window_instance = None

        self.button_canvas = None
        self.button_canvas_height = 20
        self.button_canvas_width = self.root_width

        self.configure_sizes()
        self.create_main_window()
        self.create_main_frame()
        self.create_summary_frame()

        self.create_buttons()

        self.load_images()
        self.main_frame.draw_terrain()
        self.main_frame.draw_objects()
        self.main_frame.draw_animals()

        self.display_timers_array = np.zeros([7])
        self.timer_output_file = open("output/timers.txt", "w")
        self.timer_headers = "turn    WLD    obj    pla    ff1    act    dri    ff2    unn    grw    uap    pre    " \
                             "die    sum   | DIS    wld    del    ter    obj    ani    sum    roo    idl"
        self.timer_output_file.write(self.timer_headers + "\n")

    ############################################################################################################
    def configure_sizes(self):
        self.world_height = self.num_rows * self.grid_size
        self.world_width = self.num_columns * self.grid_size

    ############################################################################################################
    def create_main_window(self):
        self.root = tk.Tk()
        self.root.resizable(0, 0)
        self.root.title("Dynamica: Turn {}".format(self.turn))

    ############################################################################################################
    def create_main_frame(self):
        self.main_frame = main_frame.MainFrame(self)
        self.main_frame.grid(row=0, column=0)

    ############################################################################################################
    def create_summary_frame(self):
        self.summary_frame = summary_frame.SummaryFrame(self)
        self.summary_frame.grid(row=0, column=1, padx=0, pady=0, ipadx=0, ipady=0)

    ############################################################################################################
    def create_buttons(self):
        self.button_canvas = button_canvas.ButtonCanvas(self)
        self.button_canvas.grid(row=1, column=0, columnspan=2, padx=0, pady=0, ipadx=0, ipady=0)

    ############################################################################################################
    def load_images(self):
        self.image_dict = {}
        ls = os.listdir('assets/images/')
        for filename in ls:
            if not filename == '.DS_Store':
                if filename[-3:] == 'gif':
                    path = 'assets/images/' + filename
                    new_image = tk.PhotoImage(file=path)
                    self.image_dict[path] = new_image

    ############################################################################################################
    def run_game(self):
        if self.running:
            self.running = False
            self.button_canvas.run_button.config(text="Run")
        else:
            self.running = True
            self.button_canvas.run_button.config(text="Pause")

        while self.running:
            self.next_turn()

    ############################################################################################################
    def next_turn(self):

        self.turn += 1
        self.root.title("Dynamica: Turn {}".format(self.turn))

        start_time = time.time()
        self.the_world.next_turn()
        self.display_timers_array[0] += time.time() - start_time

        start_time = time.time()
        self.main_frame.main_canvas.delete("all")
        self.summary_frame.summary_canvas.delete("all")
        self.display_timers_array[1] += time.time() - start_time

        start_time = time.time()
        self.main_frame.draw_terrain()
        self.display_timers_array[2] += time.time() - start_time

        start_time = time.time()
        self.main_frame.draw_objects()
        self.display_timers_array[3] += time.time() - start_time

        start_time = time.time()
        self.main_frame.draw_animals()
        self.display_timers_array[4] += time.time() - start_time

        start_time = time.time()
        self.summary_frame.update_summary_display()
        self.display_timers_array[5] += time.time() - start_time

        start_time = time.time()
        self.root.update()
        self.display_timers_array[6] += time.time() - start_time

        # if self.turn % 100 == 0:
        #     print("turn    WLD    obj    pla    ff1    act    dri    ff2    unn    grw    uap    pre    die    sum   | "
        #           "DIS    wld    del    ter    obj    ani    sum    roo")
        # if self.turn % 10 == 0:
        #     output_string = "{:5s}".format(str(self.turn))
        #     output_string += "  {:0.3f}".format(self.the_world.world_timers_array.sum())
        #     for timer in self.the_world.world_timers_array:
        #         output_string += "  {:0.3f}".format(timer)
        #     output_string += " |"
        #     output_string += "  {:0.3f}".format(self.display_timers_array.sum())
        #     for timer in self.display_timers_array:
        #         output_string += "  {:0.3f}".format(timer)
        #     print(output_string)
        #     self.the_world.world_timers_array = np.zeros([12])
        #     self.display_timers_array = np.zeros([7])
        #
        #     self.timer_output_file = open("output/timers.txt", "a")
        #     self.timer_output_file.write(output_string + "\n")
        #     self.timer_output_file.close()

    ############################################################################################################
    def save_game(self):
        pass

    ############################################################################################################
    def quit_game(self):
        if self.running:
            self.run_game()
        sys.exit(1)
