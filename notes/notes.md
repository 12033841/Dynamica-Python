## ToDo: 05/15/19

#### 1) Familiarize yourself with code base - Make comments on code to improve your understanding
#### 2) Explore different variables

## ToDo: 05/24/19
#### Making matplotlib visualization:

```python
# ToDo: Experimenting with matplotlib and calc_species_summaries to identify appropriate logic for matlotlib visualization
from src.display import display
from src import world
import matplotlib.pyplot as plt
from src.animals import animals

def main():
    the_world = world.World()
    gw = display.Display(the_world)
    # Show empty graph
    plt.figure(1, figsize=(6, 6))
    plt.plot(the_world.calc_species_summary())
    gw.root.mainloop()

main()
```

## After help from Willitz, attempt to implement visualization as described:
Also, examine new changes made to ``world.py``` file.

```python
############################################################################################################
def plot_species_summary(self):
    # Take the output from this function and use it to create three subplots for each animal's drive values
    # of the drive values that are only displayed upon clicking the animal's image on the main GUI display

    #self.species_summary_history_list

    print(self.species_summary_history_list)

'''
    create a window
    for each type fo info we care about
    create a plot and put it in the window

'''

```
