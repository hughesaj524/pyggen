from random import Random
from abc import ABCMeta, abstractmethod, abstractproperty

from .chromosome import Chromosome


class Population(metaclass=ABCMeta):
    """A generic controller class for genetic algorithms."""

    @abstractproperty
    def ChromType(self) -> "Type[C]":
        "The class used to create the population's chromosomes."
        pass
    
    @abstractproperty
    def random_seed(self) -> int:
        """The seed used to create a random generator. Ensures simulations are identical for easier testing; consistent
        randomness lets you see effects of changes more clearly. Alternately, use a randomly generated value
        (or something random-ish) for random simulations. Any hashable value works."""
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

    @abstractmethod
    def select(self) -> "Iterator[C]":
        """The selection function to be used."""
        pass

    @abstractmethod
    def cross(self, chrom1: "C", chrom2: "C") -> "C":
        """The crossover function to be used."""
        pass

    # The population of chromosomes.
    population = []
    _current_gen = -1
    
    def __init__(self) -> "P":
        self.random = Random()
        self.random.seed(self.random_seed)
        assert(self.population_size % 2 == 0)

    def __repr__(self) -> str:
        return "Population(" + str(self.get_best()) + ")"

    def get_best(self) -> "C":
        """Returns the best solution from the population."""
        return self.population[0]

    def run(self) -> "List[C]":
        """Runs the simulation."""
        while self.step():
            yield self.population

    def step(self) -> bool:
        """Progresses the population by one generation"""
        # evaluate this branch first so values like fitness of chromosomes can be used in haltcond without throwing errors
        if not(self.population):
            self.first_pop()
        elif self.halt_cond():
            return False
        else:
            self.new_pop()
        self.population
        self._current_gen += 1
        return True

    def first_pop(self):
        """Randomly generates a population of chromosomes."""
        new_pop = []
        for i in range(self.population_size):
            new_pop.append(self.ChromType(self))
        self.population = sorted(new_pop, key=lambda x: x.get_fitness())[::-1]

    def new_pop(self):
        """Produces a new generation of chromosomes from the current one. Uses UX and roulette selection by default."""
        next_pop = []

        # Copy elitism chromosomes
        for i in range(self.elitism_count):
            next_pop.append(self.population[i])

        to_zip_cross = self.select()
        to_cross = zip(to_zip_cross, to_zip_cross)                                                                                                                                                                           
        for parent1, parent2 in to_cross:
            next_pop += [self.mutate((self.cross(parent1, parent2))) for i in range(2)]

        self.population = sorted(next_pop, key=lambda x: x.get_fitness())[::-1]

    def mutate(self, chrom: "C") -> "C":
        """Mutates the chromosome according to the parent population's mutation chance."""

        for i in range(self.gene_count):
            if (self.random.random() > self.mutate_chance):
                chrom.genes ^= 1 << i

        return chrom

    # Following are some crossover functions / functions used by them that will not be called as is.
    # These are for setting to self.cross or other specific crossovers.

    def onepx(self, chrom1: "C", chrom2: "C") -> "C":
        point = self.random.randint(0, self.gene_count)
        return self.ChromType(self, (chrom1.genes&((2**point)-1))+(chrom2.genes&(2**self.gene_count-(((2**point)-1)))))

    def ux(self, chrom1: "C", chrom2: "C") -> "C":
        """Produces a child chromosome from the genes of chrom1 and chrom2 using UX crossover.

        :param chrom1: The first chromosome to cross with.
        :param chrom2: The second chromosome to cross with.
        """
        new_genes = 0
        for i in range(self.gene_count):
            new_genes |= self.random.choice((chrom1.gene_at(i), chrom2.gene_at(i))) << i
        return self.ChromType(self, new_genes)

    def roulette_select(self) -> "Iterator[C]":
        """Yields tuples of chromosomes from the population for crossover using roulette selection"""
        weighted_pop = self.weight_pop()
        for index in range(2 * int((self.population_size - self.elitism_count) / 2)):
            roulette = self.random.random()
            for i in weighted_pop.keys():
                if roulette >= i:
                    yield weighted_pop[i]
                    break
                

    def weight_pop(self) -> "Dict[float, C]":
        """Returns a dict with weighted values for roulette wheel selection."""
        self.population = sorted(self.population, key=lambda x: x.get_fitness())[::-1]
        weighted_pop = {}
        total_fitness = sum(x.get_fitness() for x in self.population)
        weighted_pop = dict(zip(map(lambda x: x.get_fitness()/total_fitness, self.population), self.population))
        return weighted_pop
