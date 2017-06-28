from generics import chromosome, population
from typing import Generic, List


class Chrom1(chromosome.Chromosome):
    def get_fitness(self):
        return self.get_genes()


class Pop1(population.Population):
    ChromType = Chrom1
    elitism_count = 2
    gene_count = 16 #highest num is 65535
    
    def halt_cond(self) -> bool:
        return self._current_gen > 100

    def select(self) -> Iterator[C]:
        return self.roulette_select()

    def cross(chrom1: Chrom1, chrom2: Chrom1) -> Chrom1:
        return self.ux(chrom1, chrom2)
    
    mutate_chance = 0.0015
    population_size = 20
    random_seed = 125


pop1 = Pop1()
chrom1 = Chrom1(pop1)

print(pop1.run())
