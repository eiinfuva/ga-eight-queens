from random import randint

class Genome:
	""" Possible solution to the N-queens problem.

		Attributes:
			numberN (int): the chromosome and chess board lenght.
			chromosome ([int]): column list where the queens are located.
	"""
	def __init__(self, numberN, chromosome):
		self.numberN = numberN
		self.chromosome = chromosome

	def calculateFitness(self):
		""" Calculate the present chromosome fitness value.
		"""
		conflicts = 0
		for i in range(self.numberN):
			if self.conflict(i, self.chromosome[i]):
				conflicts += 1
		return conflicts

	def conflict(self, row, column):
		""" Return true if the position determined by row and column is
			threated by the next queens.

			Arguments:
				row (int): the position's row that we want to check.
				column (int): the position's column that we want to check.
		"""
		for i in range(row+1, self.numberN):
			# Column check
			if (self.chromosome[i] == column):
				return True
			# Diagonal check
			if (self.chromosome[i] - column == i - row):
				return True
			if (self.chromosome[i] - column == row - i):
				return True
		return False

	def crossover(self, genome2):
		""" One point crossover between this and genome2.

			Arguments:
				genome2 (Genome): the other genome with we want to cross.
		"""
		crossPoint = randint(0, self.numberN)
		genome2.chromosome[crossPoint:], self.chromosome[crossPoint:] = \
			self.chromosome[crossPoint:], genome2.chromosome[crossPoint:]
		return (self, genome2)

	def mutate(self):
		""" Mutates a chromosome random position (or allele).
		"""
		index = randint(0, self.numberN)
		newValue = randint(0, self.numberN)
		self.chromosome[index] = newValue
