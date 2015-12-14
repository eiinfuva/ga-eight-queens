#!/usr/bin/env python
# coding=utf-8
#

from genetics.population import Population
from genetics.genome import Genome
from random import randint

def main():
    N = 8 # Size of chessboard
    n = 50 # Size of population
    max_gen = 100 # Maximum number of generations
    debug = True # Show debug flags

    population = Population(N, n)
    population.evolve(max_gen, DEBUG=debug)
    best = population.best_solution()
    print """
=====================
Mejor solución:
{}
Fitness:{}
=====================
    """.format(best,best.calculateFitness())
    # chromosome = [randint(1, N) for _ in range(N)]
    # print chromosome
    # print Genome(chromosome)

    return 0

if __name__ == '__main__':
    main()

