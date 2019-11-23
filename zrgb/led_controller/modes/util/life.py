from random import getrandbits


# one dimensional life - exactly one neighbor flips
class Life:
    def __init__(self, size, start_population=None):
        self.size = size
        self.population = start_population or self.random_population()

    def random_population(self):
        return [getrandbits(1) for _ in range(self.size)]

    def _has_one_neighbor(self, n):
        left = self.population[(n - 1) % self.size]
        right = self.population[(n + 1) % self.size]
        return left ^ right

    def new_generation(self):
        new_population = self.population.copy()
        for i in range(len(self.population)):
            if self._has_one_neighbor(i):
                new_population[i] = int(not self.population[i])
        self.population = new_population
