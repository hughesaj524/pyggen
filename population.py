from abc import ABCMeta
from chromosome import *

class Population(metaclass=ABCMeta):
    """A generic controller class for genetic algorithms."""
    
    """The seed used to create a random generator. Ensures simulations are identical for easier testing; consistent
    randomness lets you see effects of changes more clearly. Alternately, use a randomly generated value
    (or something random-ish) for random simulations."""
    random.seed(524)
