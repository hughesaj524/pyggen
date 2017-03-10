import random
from abc import ABCMeta, abstractmethod, abstractproperty


class Population(metaclass=ABCMeta):
    """A generic controller class for genetic algorithms."""
    
    """The seed used to create a random generator. Ensures simulations are identical for easier testing; consistent
    randomness lets you see effects of changes more clearly. Alternately, use a randomly generated value
    (or something random-ish) for random simulations."""
    @abstractproperty
    def random_seed(self):
        pass

    """The number of genes per chromosome."""
    @abstractproperty
    def gene_count(self):
        pass

    """The number of members in the population. Must be even because i'm garbage."""
    #FIXME: popsize must be even
    @abstractproperty
    def population_size(self):
        pass
    
    random.seed(random_seed)
    
