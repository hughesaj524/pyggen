from generics import chromosome, population


class Chrom1(chromosome.Chromosome):
    def get_fitness(self):
        return self.genes


class Pop1(population.Population):
    pass


pop1 = Pop1()
chrom1 = Chrom1(pop1)
