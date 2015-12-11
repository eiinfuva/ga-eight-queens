#!/usr/bin/env python
# coding=utf-8

r"""Population GA module.

Population of fenotypes at a genetic algorithm. The problem solved by this implementation\
is the N-Queens problem. Each fenotypes represent a permutation of N-Queens at diferent positions.

Authors:
    Sergio García.
    Daniel Gonzalez.
    Ismael Taboada.
"""

from random import randint, random


class Population:
    """Implementation of GA population.

    Implements population of fenotypes that represents table permutation of N-Queens problem.

    Attributes:
        fenotypes(int): number of fenotypes for generation.
        generation(list): set of fenotypes.
        elitism(bool): flag of elitism at genetic algorithm
        elite_len(int): number of fenotypes consider as elite
        p_c(float): probability of crossing
        p_m(float): probability of mutation
    """

    def __init__(self, N, n, elitism=False, elite_len=5, p_c=0.75, p_m=0.02):
        """Initialize class instance.

        Arguments:
            N(int): size of chessboard
            n(int): size of population
            elitism(bool): property of population elitism
            elite_len(int): if elitism, number of fenotypes consider as elite
            p_c(float): probability of crossing
            p_m(float): probability of mutation
        """
        self.fenotypes = n
        self.generation = self.initRandomPopulation(N, n)
        self.elitism = elitism
        self.elite_len = elite_len
        self.p_c = p_c
        self.p_m = p_m

    def initRandomPopulation(self, N, n):
        """Generate random fenotype population of size n.

        Arguments:
            N(int): size of board
            n(int): size of population

        Returns:
            list: set of random generated fenotypes
        """
        return [Genome(n, [randint(1, N) for _ in range(N)]) for _ in range(n)]

    def evolve(self, max_generation, finish_condition=lambda x: False):
        """Evolution process of population.

        Evolution of genetic algorithm lead by a number of maximum generations or a finish condition.

        Arguments:
            max_generation(int): maximum number of generations
            finish_condition(function): finish con
        """
        for _ in range(max_generation):  # Iteration for each generation
            next_generation = []

            if self.elitism:  # Resolve elitism
                self.generation.sort(key=lambda gen: gen.calculateFitness())  # sorted by fitness
                next_generation.extend([self.generation.pop(0) for _ in self.elite_len])

            while len(next_generation) < self.fenotypes:  # Until next generation if fill

                parent_a, parent_b = self.selection  # Select predecessors

                if random() < self.p_c:  # If crossing
                    child_a, child_b = parent_a.crossOver(parent_b)  # Generate offspring

                    # Mutate offspring
                    if random() < self.p_m: child_a.mutate()
                    if random() < self.p_m: child_b.mutate()
                    next_generation.extend([child_a, child_b])  # Introduce into next generation

                else:  # If not crossing, parents copy to next generation
                    next_generation.extend([parent_a, parent_b])

            self.generation = []  # Next_generation as actual population
            self.generation.extend(next_generation)

            min_fitness = reduce(lambda x, y: min(x.calculateFitness(), y.calculateFitness()),
                                 self.generation)  # Calculate minimun fitness value

            if min_fitness == 0:  # Evaluate optimal solution at any fenotypes
                break

            if finish_condition(self.generation):  # Evaluate finish statement
                break

    def selection(self):
        """Selection of two fenotypes from population.

        Selection of predecessors for next generation. First selected by tournament, second selected by roulette.

        Returns:
            Genome, Genome: two fenotypes selected from population.
        """
        # TODO: selection by tournament and roulette
        return self.generation.pop(0), self.generation.pop(0)

    def best_solution(self):
        """Population best fenotype.

        Returns:
            Genome: best fenotype of population evaluated by fitness.
        """
        self.generation.sort(key=lambda x: x.calculateFitness())
        return self.generation[0]
