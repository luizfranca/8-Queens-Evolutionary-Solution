import random

class Board:
	def __init__(self):
		self.board = []
		aux = range(8)
		for i in xrange(8):
			element = random.randint(0, len(aux) - 1)
		 	self.board += [aux[element]]
			del aux[element] 

	def fitness(self):
		score = 0

		for i in range(len(self.board)):
			aux = self.board[i]
			for j in range(len(self.board)):
				if i == j:
					continue
				if self.board[i] == self.board[j]:
					score += 1

				distance = j - i

				if (self.board[i] + distance == self.board[j]): 
					score += 1
				if (self.board[i] - distance == self.board[j]):
					score += 1

		return score

	def mutate(self):
		probMutation = random.randint(0, 100)

		if (probMutation > 80):
			return

		swapPoint1 = random.randint(0, 7)
		swapPoint2 = random.randint(0, 7)

		self.board[swapPoint1], self.board[swapPoint2] = self.board[swapPoint2], self.board[swapPoint1]

def getKey(element):
		return element.fitness()

class AE():
	def __init__(self, pop = 30):
		self.boards = []
		self.pop = pop

		for i in xrange(pop):
			self.boards += [Board()]

	def select(self):
		selected = []

		numberSelection = self.pop * 0.4

		while(len(selected) < numberSelection):
			element = self.boards[random.randint(0, len(self.boards) - 1)]

			if (not element in selected):
				selected += [element]

		return selected 

	def crossover(self, selected):
		children = []

		for i in range(0 ,len(selected) / 2, 2):
			cutPoint = random.randint(0, 7)

			child1 = Board()
			child1.board = selected[i].board[:cutPoint] + selected[i + 1].board[cutPoint:]
			child1.mutate()

			child2 = Board()
			child2.board = selected[i].board[cutPoint:] + selected[i + 1].board[:cutPoint]
			child2.mutate()

			children += [child1, child2]

		return children

	def sortBoards(self):
		self.boards = sorted(self.boards, key=getKey)

	def meanFitness(self):
		score = 0.0
		for i in self.boards:
			score += i.fitness()
		return score / self.pop

	def printBoard(self, board):
		print board.board
		print "fitness: %6d mean fitness: %6.2f" % (board.fitness(), self.meanFitness())

	def printBoards(self):
		for i in self.boards:
			self.printBoard(i)

	def run(self):
		bestFitness = 1000
		gen = 0

		print ("=" * 50) + " generation: " + str(gen)
		self.printBoard(self.boards[0])

		while (bestFitness != 0):
			selected = self.select() # seleciona os pais

			children = self.crossover(selected) # gera os filhos

			self.boards += children # adiciona os filhos na populacao

			self.sortBoards() # ordena a popuulacao

			self.boards = self.boards[:self.pop] # elimina os piores elementos da populacao

			curFitness = self.boards[0].fitness()
			if (bestFitness > curFitness): 
				bestFitness = curFitness

			gen += 1

			print ("=" * 50) + " generation: " + str(gen) # imprime a geracao 
			self.printBoard(self.boards[0]) # imprime o melhor elemento da populacao
			#self.printBoards()             # imprime a populacao
		#print ("=" * 50) + " generation: " + str(gen)
		#self.printBoard(self.boards[0])
		

ae = AE(30)
ae.run()