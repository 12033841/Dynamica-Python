import tkinter as tk
from src.display import species_info_window


class SummaryFrame(tk.Frame):
    ############################################################################################################
    def __init__(self, display):
        tk.Frame.__init__(self,
                           )

        self.summary_canvas = tk.Canvas(self,
                                        width=display.summary_canvas_width, height=display.summary_canvas_height,
                                        bg="white", bd=2, highlightthickness=0)
        self.summary_canvas.grid(row=0, column=0)

        self.display = display
        self.summary_canvas_width = display.summary_canvas_width
        self.summary_canvas_height = display.summary_canvas_height

        self.lion_image = tk.PhotoImage(file='assets/images/Lion0.gif')
        self.grass_image = tk.PhotoImage(file='assets/images/plains.gif')
        self.zebra_image = tk.PhotoImage(file='assets/images/Zebra0.gif')

        self.summary_main_title = None
        self.summary_plant_title = None
        self.plant_image_label = None
        self.plant_text_label = None
        self.summary_animal_title = None
        self.zebra_text_label = None
        self.lion_text_label = None
        self.zebra_image_label = None
        self.lion_image_label = None

        self.create_summary_display()

    ############################################################################################################
    def create_summary_display(self):
        # create the summary display main title
        self.summary_main_title = tk.Label(self.summary_canvas, text="Dynamica Summary", font="Verdana 16 bold", anchor=tk.W)
        self.summary_main_title.place(x=10, y=10)

        # create the plants display
        # create the grass label
        self.summary_plant_title = tk.Label(self.summary_canvas, text="Plants", font="Verdana 12 bold", anchor=tk.W)
        self.summary_plant_title.place(x=10, y=50)

        # get and place the grass image
        self.plant_image_label = tk.Label(self.summary_canvas, image=self.grass_image, anchor=tk.W)
        self.plant_image_label.place(x=30, y=80)

        # get and place the grass data, or fill in zeros if no grass
        if 'Grass' in self.display.the_world.turn_summary_dict['Plant']:
            grass_data = self.display.the_world.turn_summary_dict['Plant']['Grass']
            plant_text_string = "Grass     Tiles: {}    Qty: {:3.2f}%".format(grass_data[0], 100 * (
                    grass_data[1] / (grass_data[0] * 100)))
        else:
            plant_text_string = "Grass     Tiles: 0    Qty: 0"
        self.plant_text_label = tk.Label(self.summary_canvas, text=plant_text_string, font="Verdana 10", anchor=tk.W)
        self.plant_text_label.place(x=70, y=90)

        # create the animals display
        self.summary_animal_title = tk.Label(self.summary_canvas, text="Animals", font="Verdana 12 bold", anchor=tk.W)
        self.summary_animal_title.place(x=10, y=150)

        # create the zebra display
        # get and place the zebra image

        self.zebra_image_label = tk.Label(self.summary_canvas, image=self.zebra_image, anchor=tk.W)
        self.zebra_image_label.place(x=30, y=180)

        if 'Zebra' in self.display.the_world.turn_summary_dict['Animal']:
            zebra_data = self.display.the_world.turn_summary_dict['Animal']['Zebra']
            qty = str("{:0.0f}".format(zebra_data[0]))
            health = str("{:3.2f}".format(zebra_data[1]))
            energy = str("{:3.2f}".format(zebra_data[2]))
            arousal = str("{:3.2f}".format(zebra_data[3]))
            zebra_text_string = "Zebra   Qty: {:5s}   ".format(qty)
            zebra_text_string += "Health: {:<7s}    ".format(health)
            zebra_text_string += "Energy: {:<7s}    ".format(energy)
            zebra_text_string += "Arousal: {:<7s}    ".format(arousal)
        else:
            zebra_text_string = "Zebra   Qty: 0   Health: NA   Energy: NA    Arousal: NA"

        self.zebra_text_label = tk.Label(self.summary_canvas, text=zebra_text_string, font="Verdana 10", anchor=tk.W)
        self.zebra_text_label.place(x=70, y=190)
        self.zebra_image_label.bind('<Double-Button-1>', self.animal_summary_on_double_click)
        self.zebra_text_label.bind('<Double-Button-1>', self.animal_summary_on_double_click)

        # create the lion display
        # get and place the zebra image

        self.lion_image_label = tk.Label(self.summary_canvas, image=self.lion_image, anchor=tk.W)
        self.lion_image_label.place(x=30, y=220)

        if 'Lion' in self.display.the_world.turn_summary_dict['Animal']:
            lion_data = self.display.the_world.turn_summary_dict['Animal']['Lion']
            qty = str("{:0.0f}".format(lion_data[0]))
            health = str("{:3.2f}".format(lion_data[1]))
            energy = str("{:3.2f}".format(lion_data[2]))
            arousal = str("{:3.2f}".format(lion_data[3]))
            lion_text_string = "Lion   Qty: {:5s}   ".format(qty)
            lion_text_string += "Health: {:<7s}    ".format(health)
            lion_text_string += "Energy: {:<7s}    ".format(energy)
            lion_text_string += "Arousal: {:<7s}    ".format(arousal)
        else:
            lion_text_string = "Lion   Qty: 0   Health: NA   Energy: NA    Arousal: NA"

        self.lion_text_label = tk.Label(self.summary_canvas, text=lion_text_string, font="Verdana 10", anchor=tk.W)
        self.lion_text_label.place(x=70, y=230)
        self.lion_text_label.bind('<Double-Button-1>', self.animal_summary_on_double_click)
        self.lion_text_label.bind('<Double-Button-1>', self.animal_summary_on_double_click)

    ############################################################################################################
    def update_summary_display(self):
        self.summary_main_title.destroy()
        self.summary_plant_title.destroy()
        self.plant_image_label.destroy()
        self.plant_text_label.destroy()
        self.summary_animal_title.destroy()
        self.zebra_text_label.destroy()
        self.lion_text_label.destroy()
        self.zebra_image_label.destroy()
        self.lion_image_label.destroy()

        # create the summary display main title
        self.summary_main_title = tk.Label(self.summary_canvas, text="Dynamica Summary", font="Verdana 16 bold", anchor=tk.W)
        self.summary_main_title.place(x=10, y=10)

        # create the plants display
        # create the grass label
        self.summary_plant_title = tk.Label(self.summary_canvas, text="Plants", font="Verdana 12 bold", anchor=tk.W)
        self.summary_plant_title.place(x=10, y=50)

        # get and place the grass image
        self.plant_image_label = tk.Label(self.summary_canvas, image=self.grass_image, anchor=tk.W)
        self.plant_image_label.place(x=30, y=80)

        # get and place the grass data, or fill in zeros if no grass
        if 'Grass' in self.display.the_world.turn_summary_dict['Plant']:
            grass_data = self.display.the_world.turn_summary_dict['Plant']['Grass']
            plant_text_string = "Grass     Tiles: {}    Qty: {:3.2f}%".format(grass_data[0], 100 * (
                    grass_data[1] / (grass_data[0] * 100)))
        else:
            plant_text_string = "Grass     Tiles: 0    Qty: 0"
        self.plant_text_label = tk.Label(self.summary_canvas, text=plant_text_string, font="Verdana 10", anchor=tk.W)
        self.plant_text_label.place(x=70, y=90)

        # create the animals display
        self.summary_animal_title = tk.Label(self.summary_canvas, text="Animals", font="Verdana 12 bold", anchor=tk.W)
        self.summary_animal_title.place(x=10, y=150)

        # create the zebra display
        # get and place the zebra image

        self.zebra_image_label = tk.Label(self.summary_canvas, image=self.zebra_image, anchor=tk.W)
        self.zebra_image_label.place(x=30, y=180)

        if 'Zebra' in self.display.the_world.turn_summary_dict['Animal']:
            zebra_data = self.display.the_world.turn_summary_dict['Animal']['Zebra']
            qty = str("{:0.0f}".format(zebra_data[0]))
            health = str("{:3.2f}".format(zebra_data[1]))
            energy = str("{:3.2f}".format(zebra_data[2]))
            arousal = str("{:3.2f}".format(zebra_data[3]))
            zebra_text_string = "Zebra   Qty: {:5s}   ".format(qty)
            zebra_text_string += "Health: {:<7s}    ".format(health)
            zebra_text_string += "Energy: {:<7s}    ".format(energy)
            zebra_text_string += "Arousal: {:<7s}    ".format(arousal)
        else:
            zebra_text_string = "Zebra   Qty: 0   Health: NA   Energy: NA    Arousal: NA"

        self.zebra_text_label = tk.Label(self.summary_canvas, text=zebra_text_string, font="Verdana 10", anchor=tk.W)
        self.zebra_text_label.place(x=70, y=190)
        self.zebra_image_label.bind('<Double-Button-1>', self.animal_summary_on_double_click)
        self.zebra_text_label.bind('<Double-Button-1>', self.animal_summary_on_double_click)

        # create the lion display
        # get and place the zebra image

        self.lion_image_label = tk.Label(self.summary_canvas, image=self.lion_image, anchor=tk.W)
        self.lion_image_label.place(x=30, y=220)

        if 'Lion' in self.display.the_world.turn_summary_dict['Animal']:
            lion_data = self.display.the_world.turn_summary_dict['Animal']['Lion']
            qty = str("{:0.0f}".format(lion_data[0]))
            health = str("{:3.2f}".format(lion_data[1]))
            energy = str("{:3.2f}".format(lion_data[2]))
            arousal = str("{:3.2f}".format(lion_data[3]))
            lion_text_string = "Lion   Qty: {:5s}   ".format(qty)
            lion_text_string += "Health: {:<7s}    ".format(health)
            lion_text_string += "Energy: {:<7s}    ".format(energy)
            lion_text_string += "Arousal: {:<7s}    ".format(arousal)
        else:
            lion_text_string = "Lion   Qty: 0   Health: NA   Energy: NA    Arousal: NA"

        self.lion_text_label = tk.Label(self.summary_canvas, text=lion_text_string, font="Verdana 10", anchor=tk.W)
        self.lion_text_label.place(x=70, y=230)
        self.lion_text_label.bind('<Double-Button-1>', self.animal_summary_on_double_click)
        self.lion_text_label.bind('<Double-Button-1>', self.animal_summary_on_double_click)

    ############################################################################################################
    def animal_summary_on_double_click(self, event):
        print("Species click event", event)
        species = 'Zebra'
        if self.display.species_summary_window is not None:
            self.display.species_summary_window.destroy()
        self.display.species_summary_window = tk.Toplevel(self.display.root)
        self.species_summary_window_instance = species_info_window.SpeciesInfoWindow(self.display.species_summary_window,
                                                                                     self.display.the_world, species)




