#!/usr/bin/env python
# coding=utf-8
#

from genetics.population import Population
from genetics.genome import Genome
from random import randint

def main():
    N = 8 # Size of chessboard
    n = 16 # Size of population
    max_gen = 100 # Maximum number of generations
    debug = True # Show debug flags

    # population = Population(N, n, elitism=True, elite_len=5, p_c=0.7, p_m=0.2)
    population = Population(N, n, p_c=0.7, p_m=0.05)
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

