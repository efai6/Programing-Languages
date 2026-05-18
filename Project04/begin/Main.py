from World import World
from Position import Position
from Organisms.Organism import Organism
from Organisms.Grass import Grass
from Organisms.Sheep import Sheep
from Organisms.Lynx import Lynx
from Organisms.Antelope import Antelope
import os

def getConcreteOrganisms(base_class):
	subclasses = base_class.__subclasses__()

	if not subclasses:
		return [base_class]
	
	concrete_classes = []
	for sub in subclasses:
		concrete_classes.extend(getConcreteOrganisms(sub))
        
	return concrete_classes


if __name__ == '__main__':
	pyWorld = World(10, 10)
	

	newOrg = Grass(position=Position(xPosition=9, yPosition=9), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	newOrg = Grass(position=Position(xPosition=1, yPosition=1), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	newOrg = Sheep(position=Position(xPosition=6, yPosition=4), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	newOrg = Lynx(position=Position(xPosition=3, yPosition=4), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	newOrg = Antelope(position=Position(xPosition=5	, yPosition=4), world=pyWorld)
	pyWorld.addOrganism(newOrg)
	
	available_creatures = getConcreteOrganisms(Organism)
	print(pyWorld)

	for _ in range(0, 50):
		user_input = input("Enter a command to proceed:[Enter] to continue simulation, [p] to enable plague, [spawn] to enter a organism spawn menu: ").strip().lower()
		if user_input == 'p':
			pyWorld.Plague()
		elif user_input == 'spawn':
			for i, cls in enumerate(available_creatures):
				print(f"Organisms availaible to add: [{i}] - {cls.__name__}")
			animal_choice = int(input("Enter a number of an animal you would like to add: "))
			x_pos = int(input("Enter a position X: "))
			y_pos = int(input("Enter a position Y: "))
			target_position = Position(xPosition=x_pos, yPosition=y_pos)
			if pyWorld.positionOnBoard(target_position) and pyWorld.getOrganismFromPosition(target_position) is None:
				SelectedClass = available_creatures[animal_choice]
				new_org = SelectedClass(position=target_position, world=pyWorld)
				pyWorld.addOrganism(new_org)
				print(f"{SelectedClass.__name__} was added")
			else:
				print("The place is taken by another organism or the coordinates given exceed  size of the map")
			continue
		pyWorld.makeTurn()
		print(pyWorld)
