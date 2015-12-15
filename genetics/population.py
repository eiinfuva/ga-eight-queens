#!/usr/bin/env python
# coding=utf-8

r"""Population GA module.

Population of fenotypes at a genetic algorithm. The problem solved by this implementation\
is the N-Queens problem. Each fenotypes represent a permutation of N-Queens at different positions.

Authors:
    Sergio García.
    Daniel Gonzalez.
    Ismael Taboada.
"""

from random import randint, random
from genome import Genome
import logging
import os

DEBUG = False
LOG_FILE = 'ga_n_queens.log'

if os._exists(LOG_FILE):
    os.system('rm '+LOG_FILE)

logging.basicConfig(filename=LOG_FILE, filemode='w', level=logging.DEBUG)


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

    def __init__(self, N_chessboard, n_population, elitism=False, elite_len=6, p_c=0.7, p_m=0.05):
        """Initialize class instance.

        Arguments:
            N_chessboard(int): size of chessboard
            n_population(int): size of population
            elitism(bool): property of population elitism
            elite_len(int): if elitism, number of fenotypes consider as elite
            p_c(float): probability of crossing
            p_m(float): probability of mutation
        """
        self.fenotypes = n_population
        self.generation = self.initRandomPopulation(N_chessboard, n_population)
        self.elitism = elitism
        self.elite_len = elite_len
        self.p_c = p_c
        self.p_m = p_m

    def initRandomPopulation(self, N_chessboard, n_population):
        """Generate random fenotype population of size n.

        Arguments:
            N_chessboard(int): size of board
            n_population(int): size of population

        Returns:
            list: set of random generated fenotypes
        """
        population = []
        while len(population) < n_population:
            rand_chromosome = [randint(1, N_chessboard) for _ in range(N_chessboard)]
            while rand_chromosome in population:
                rand_chromosome = [randint(1, N_chessboard) for _ in range(N_chessboard)]
            population.append(Genome(rand_chromosome))
        return population

    def evolve(self, max_generation, finish_condition=lambda x: False, DEBUG=False):
        """Evolution process of population.

        Evolution of genetic algorithm lead by a number of maximum generations or a finish condition.

        Arguments:
            max_generation(int): maximum number of generations
            finish_condition(function): finish con
        """
#         if DEBUG:
#             print """
# ========================
# Initial generation:
#             """
#             for index, fenotype in enumerate(self.generation):
#                 print "-------------\nFenotype #{}:\n{}\nFitness:{}\n".format(index + 1, fenotype,
#                                                                               fenotype.calculateFitness())

        for n_generation in range(max_generation):  # Iteration for each generation
            next_generation = []
            sum_cross = sum_mut = 0

            if self.elitism:  # Resolve elitism
                self.generation.sort(key=lambda gen: gen.calculateFitness())  # sorted by fitness
                next_generation.extend([self.generation.pop(0) for _ in range(self.elite_len)])
                if DEBUG:
                    logging.debug("Elitism: Elite: [%s]",
                                  ','.join(["[%s](%d)" % (','.join(map(str, elem.chromosome)), elem.calculateFitness())
                                            for elem in next_generation]))

            while len(next_generation) < self.fenotypes:  # Until next generation if fill

                parent_a, parent_b = self.selection()  # Select predecessors

                if random() < self.p_c:  # If crossing
                    child_a, child_b = parent_a.crossOver(parent_b)  # Generate offspring
                    if DEBUG:
                        logging.debug("Crossing: Parents: [%s](%d), [%s](%d)",
                                      ','.join(map(str, parent_a.chromosome)), parent_a.calculateFitness(),
                                      ','.join(map(str, parent_b.chromosome)), parent_b.calculateFitness())
                        logging.debug("Crossing: Offspring: [%s](%d), [%s](%d)",
                                      ','.join(map(str, child_a.chromosome)), child_a.calculateFitness(),
                                      ','.join(map(str, child_b.chromosome)), child_b.calculateFitness())
                    sum_cross += 1
                    # Mutate offspring
                    if random() < self.p_m:
                        child_a.mutate()
                        sum_mut += 1
                        if DEBUG: logging.debug(
                                "Mutation: Child_a: [%s](%d)", ','.join(map(str, child_a.chromosome)),
                                child_a.calculateFitness())
                    if random() < self.p_m:
                        child_b.mutate()
                        sum_mut += 1
                        if DEBUG:
                            logging.debug(
                                    "Mutation: Child_a: [%s](%d)", ','.join(map(str, child_b.chromosome)),
                                    child_b.calculateFitness())
                    next_generation.extend([child_a, child_b])  # Introduce into next generation

                else:  # If not crossing, parents copy to next generation
                    if DEBUG:
                        logging.debug("Copied: Parents: [%s](%d), [%s](%d)",
                                      ','.join(map(str, parent_a.chromosome)), parent_a.calculateFitness(),
                                      ','.join(map(str, parent_b.chromosome)), parent_b.calculateFitness())
                    next_generation.extend([parent_a, parent_b])

            self.generation = []  # Next_generation as actual population
            self.generation.extend(next_generation)

            fitness = map(lambda x: x.calculateFitness(), self.generation)

            min_fitness = min(fitness)  # Calculate minimun fitness value
            avg_fitness = float(sum(fitness)) / float(len(fitness))

            if min_fitness == 0:  # Evaluate optimal solution at any fenotypes
                break

            if finish_condition(self.generation):  # Evaluate finish statement
                break
            if DEBUG:
                logging.info("Generación#%d min_fitness:%d avg_fitness:%d\n\tcruces:%d mutaciones:%d", n_generation,
                             min_fitness,
                             avg_fitness,
                             sum_cross,
                             sum_mut)
                # print """
                # ========================
                # Generation #{}:
                # """.format(n_generation)
                # for index, fenotype in enumerate(self.generation):
                #    print "-------------\nFenotype #{}:\n{}\nFitness:{}\n".format(index, fenotype,
                #                                                                fenotype.calculateFitness())

    def selection(self):
        """Selection of two fenotypes from population.

        Selection of predecessors for next generation. First selected by tournament, second selected by roulette.

        Returns:
            Genome, Genome: two fenotypes selected from population.
        """
        self.generation.sort(key=lambda gen: gen.calculateFitness())  # sorted by fitness
        genome1 = genome2 = None

        # tournament selection
        fenotypes = []

        for i in range(2):  # 2 parents
            fenotypes.append(randint(0, len(self.generation) - 1))  # get random index to fenotype
        genome1 = self.generation.pop(min(fenotypes))  # extract the fenotype with best fitness

        # genome1 = self.generation.pop(sorted(fenotypes,key=lambda x: x.calculateFitness()))  # extract the fenotype with best fitness

        # roulette selection
        totalFitness = 0.0
        proportions = map(lambda x: 1.0 / float(x.calculateFitness()),
                          self.generation)  # list of fitness inverse for each fenotype
        totalFitness = sum(proportions)  # Total sum of fitness
        sumP = 0
        for i in range(len(proportions)):  # Calculate accumulated fitness of each roulette's section.
            sumP += proportions[i] / totalFitness
            proportions[i] = sumP

        selection = random()  # Select random fitness
        for i in range(len(proportions)):  # Select one position and gets the section
            if (selection < proportions[i]):
                genome2 = self.generation.pop(i)  # extract the section's fenotype
                break

        return genome1, genome2

    def best_solution(self):
        """Population best fenotype.

        Returns:
            Genome: best fenotype of population evaluated by fitness.
        """
        self.generation.sort(key=lambda x: x.calculateFitness())
        return self.generation[0]
