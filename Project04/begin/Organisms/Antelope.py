from .Animal import Animal
from Action import Action
from ActionEnum import ActionEnum
import random
from Position import Position

class Antelope(Animal):

	def __init__(self, sheep=None, position=None, world=None):
		super(Antelope, self).__init__(sheep, position, world)

	def clone(self):
		return Antelope(self, None, None)

	def initParams(self):
		self.power = 4
		self.initiative = 3
		self.liveLength = 11
		self.powerToReproduce = 5
		self.sign = 'A'

	def getNeighboringPosition(self):
		return self.world.filterPositionsWithoutAnimals(self.world.getNeighboringPositions(self.position))
	
	def senseOfPredator(self,position):
		neighbors = self.world.getNeighboringPositions(position)

		predator_position = None
		for pos in neighbors:
			org = self.world.getOrganismFromPosition(pos)
			if org.__class__.__name__ == "Lynx":
				predator_position = pos
				break
		return predator_position
	
	def move(self):
		predator_position = self.senseOfPredator(self.position)
		if predator_position:
			movingVector = ((predator_position.x - self.position.x) * (-2) , (predator_position.y - self.position.y) * (-2))
			candidatePosition = Position(xPosition = self.position.x + movingVector[0], yPosition = self.position.y + movingVector[1])
			if self.world.positionOnBoard(candidatePosition) and self.world.getOrganismFromPosition(candidatePosition) is None and self.senseOfPredator(candidatePosition) is None:
				self.lastPosition = self.position
				print(f"Antelope spotted predator on {predator_position} and ran away from {self.position} to {candidatePosition}")
				return [Action(ActionEnum.A_MOVE, candidatePosition, 0, self)]
			else: return[Action(ActionEnum.A_MOVE, predator_position, 0, self)]
		return super(Antelope, self).move()
		'''inny algorytm ucieczki antylopy'''
		# if predator_position:
		# 	escape_directions = [(1,0), (0,1), (1,1), (-1,-1), (-1,0), (-1,1), (1,-1), (0,-1)]
		# 	for dx,dy in (escape_directions):
		# 		if (predator_position.x - self.position.x) == dx and (predator_position.y - self.position.y) == dy:
		# 			continue
		# 		movingVector = (dx * 2, dy * 2)
		# 		candidatePosition = Position(self.position.x + movingVector[0], self.position.y + movingVector[1])
		# 		if self.world.positionOnBoard(candidatePosition) and self.world.getOrganismFromPosition(candidatePosition) is None and self.senseOfPredator(candidatePosition) is None:
		# 			self.lastPosition = self.position
		# 			return [Action(ActionEnum.A_MOVE, candidatePosition, 0, self)]
