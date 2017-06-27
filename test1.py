from generics import chromosome, population


class Chrom1(chromosome.Chromosome):
    def get_fitness(self):
        return self.get_genes()


class Pop1(population.Population):
    ChromType = Chrom1
    elitism_count = 2
    gene_count = 16
    
    def halt_cond(self) -> bool:
        return self._current_gen > 100
    
    mutate_chance = 0.0015
    population_size = 20
    random_seed = 125


pop1 = Pop1()
chrom1 = Chrom1(pop1)

print(pop1.run())
