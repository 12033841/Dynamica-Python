from src import config
import numpy as np


class Phenotype:
    ############################################################################################################
    def __init__(self, animal):
        self.animal = animal
        self.trait_gene_size_dict = config.Animal.trait_gene_size_dict

        self.num_traits = None
        self.trait_list = None
        self.trait_index_dict = None
        self.trait_value_dict = None

        self.init_traits()

    ############################################################################################################
    def __repr__(self):
        output_string =  "Phenotype: {} Traits\n".format(self.num_traits)
        for trait in self.trait_value_dict:
            if isinstance(self.trait_value_dict[trait], np.ndarray):
                value = ""
                for e in self.trait_value_dict[trait]:
                    if e.is_integer():
                        value += "{:0.0f} ".format(e)
                    else:
                        value += "{:0.2f} ".format(e)
                value = value[:-1]
            elif isinstance(self.trait_value_dict[trait], float):
                value = "{:0.3f}".format(self.trait_value_dict[trait])
            else:
                value = self.trait_value_dict[trait]
            output_string += "    {:24s}: {}\n".format(trait, str(value))
        return output_string

    ############################################################################################################
    def init_traits(self):

        self.num_traits = 0
        self.trait_list = []
        self.trait_index_dict = {}
        self.trait_value_dict = {}

        for trait in self.trait_gene_size_dict:

            self.trait_list.append(trait)
            self.trait_index_dict[trait] = self.num_traits
            self.num_traits += 1

            gene = self.animal.genome.gene_list[self.animal.genome.gene_index_dict[trait]]
            if self.trait_gene_size_dict[trait][1] == 'sum':
                self.trait_value_dict[trait] = gene.sum()

            elif self.trait_gene_size_dict[trait][1] == 'mean':
                self.trait_value_dict[trait] = round(gene.mean(), 6)

            elif self.trait_gene_size_dict[trait][1] == 'binary':
                self.trait_value_dict[trait] = int(np.array2string(gene, separator="")[1:-1], 2)

            elif self.trait_gene_size_dict[trait][1] == 'inv_binary':
                self.trait_value_dict[trait] = round(1 / (int(np.array2string(gene, separator="")[1:-1], 2) + 1), 6)

            elif self.trait_gene_size_dict[trait][1] == 'direction':
                if gene.sum() > 0:
                    self.trait_value_dict[trait] = 1
                else:
                    self.trait_value_dict[trait] = -1

            elif self.trait_gene_size_dict[trait][1] == 'vector':
                self.trait_value_dict[trait] = gene
