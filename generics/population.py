import random
from abc import ABCMeta, abstractmethod, abstractproperty

from .chromosome import Chromosome

class Population(metaclass=ABCMeta):
    """A generic controller class for genetic algorithms."""

    @abstractproperty
    def ChromType(self) -> "class":
        "The class used to create the population's chromosomes."
        pass
    
    @abstractproperty
    def random_seed(self) -> int:
        """The seed used to create a random generator. Ensures simulations are identical for easier testing; consistent
        randomness lets you see effects of changes more clearly. Alternately, use a randomly generated value
        (or something random-ish) for random simulations."""
        pass
    
    @abstractproperty
    def gene_count(self) -> int:
        """The number of genes per chromosome."""
        pass
    
    @abstractproperty
    def population_size(self) -> int:
        """The number of members in the population. Must be even because i'm garbage."""
        pass

    @abstractproperty
    def mutate_chance(self) -> float:
        """The chance out of 1 that each gene will mutate. Around 0.0015"""
        pass

    @abstractproperty
    def elitism_count(self) -> int:
        """The number of "best" solutions copied from one generation to the next. 0 is fine."""
        pass

    @abstractmethod
    def halt_cond(self) -> bool:
        """Returns true if the current generation is the final one."""
        pass
    
    random.seed(random_seed)

    # The population of chromosomes.
    population = []
    _current_gen = -1
    
    def __init__(self):
        assert(self.population_size % 2 == 0)

    def __repr__(self):
        return "Population(" + str(self.population) + ")"

    def get_best(self) -> Chromosome:
        """Returns the best solution from the population."""
        return self.population[0]

    def run(self) -> [Chromosome]:
        while self.step():
            yield self.population

    def step(self) -> bool:
        # evaluate this branch first so values like fitness of chromosomes can be used in haltcond without throwing errors
        if not(self.population):
            new_pop = []
            for i in range(self.population_size):
                new_pop.append(self.ChromType(self))
            self.population = sorted(new_pop, key=lambda x: x.get_fitness())
        elif self.halt_cond():
            return False
        else:
            self.new_pop()
        print(self.population)
        self._current_gen += 1
        return True

    def new_pop(self):
        """Produces a new generation of chromosomes from the current one. Uses UX and roulette selection by default."""
        next_pop = []

        # Copy elitism chromosomes
        for i in range(self.elitism_count):
            next_pop.append(self.population[i])

        to_zip_cross = self.roulette_select()
        to_cross = zip(to_zip_cross, to_zip_cross)                                                                                                                                                                           
        for parent1, parent2 in to_cross:
            next_pop += [parent1.ux(parent2) for i in range(2)]

        self.population = sorted(next_pop, key=lambda x: x.get_fitness())

    def roulette_select(self):
        """Yields tuples of chromosomes from the population for crossover using roulette selection"""
        weighted_pop = self.weight_pop()
        for index in range(int((self.population_size - self.elitism_count) / 2)):
            roulette = random.random()
            for i in weighted_pop.keys():
                if roulette >= i:
                    yield weighted_pop[i]
                    break

    def weight_pop(self) -> "Dict[Double, C]":
        """Returns a dict with weighted values for roulette wheel selection."""
        weighted_pop = {}
        for i in range(len(self.population)):
            weighted_pop[float(1 / (i + 1))] = self.population[i]
        return weighted_pop
