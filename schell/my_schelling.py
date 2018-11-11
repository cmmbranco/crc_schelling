import matplotlib.pyplot as plt
import random
import numpy as np
import math

def plotboard(board, agentlist, title, file_name):
	fig, ax = plt.subplots()
	#If you want to run the simulation with more than 7 colors, you should set agent_colors accordingly
	agent_colors = {0:'b', 1:'r', 2:'g', 3:'c', 4:'m', 5:'y', 6:'k'}
	for agent in agentlist:
		x = agent.getX()+0.5
		y = agent.getY()+0.5
		ax.scatter(x, y, color=agent_colors[agent.getRace()])

	ax.set_title(title, fontsize=10, fontweight='bold')
	ax.set_xlim([0, board.getWidth()])
	ax.set_ylim([0, board.getHeight()])
	ax.set_xticks([])
	ax.set_yticks([])
	#ax.show()
	plt.savefig(file_name)


class Agent:
	def __init__(self, race, tolerance, x , y):
		self.tolerance = tolerance
		self.race=race
		self.x = x
		self.y = y


	def getAtribs(self):
		ret = {}
		
		ret['race'] = self.race
		ret['tolerance'] = self.tolerance

		return ret


	def setPair(self, pair):
		self.x = pair[0]
		self.y = pair[1]

	def setX(self,x):
		self.x = x

	def setY(self, y):
		self.y = y

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def getRace(self):
		return self.race

	def setrRace(self,race):
		self.race = race

	
	def rankDif(self, agent):
		#can return some more complicated difference
		#implement via strategy pattern
		agentatribs = agent.getAtribs()
		if agentatribs['race'] == self.race:
			return 0
		else:
			return 1
		

	def is_happy(self, board):
		
		total = 0
		like_me = 0
		neigh_values = []

		for x in (-1,0,1):
			for y in (-1,0,1):
				boardwidth = board.getWidth()
				boardheight = board.getHeight()
				if self.getX()+x >=0 and self.getY()+y>= 0 and self.getX()+x < boardwidth and self.getY()+y < boardheight:
					pair = (self.getX()+x, self.getY()+y)
					neigh_values.append(pair)


		for cell in neigh_values:
			neighbour = board.getAgent(cell[0],cell[1])
			if neighbour == 0:
				pass

			elif self.rankDif(neighbour) == 0:
				total += 1
				like_me += 1
			else:
				total+=1


		if (like_me/total) < self.tolerance:
			return False
		else:
			return True



class Board:

	def __init__(self,width,height,empty_ratio,n_iter):
		self.width = width
		self.height = height
		self.empty_ratio = empty_ratio

	def printBoard(self):
		print('a board')

	def create(self):

		self.matrix = [[0 for x in range(self.width)] for y in range(self.height)]

		self.empty_houses = []
		self.n_empty = int(math.ceil(self.empty_ratio * self.width * self.height ))
		
		for i in range(self.n_empty):
			x = random.randint(0,self.width-1)
			y = random.randint(0,self.height-1)
			pair = (x,y)
			self.empty_houses.append(pair)
		
	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height

	def addAgent(self, agent):
		self.matrix[agent.getX()][agent.getY()] = agent
		pair = (agent.getX(), agent.getY())
		if pair in self.empty_houses:
			self.empty_houses = np.delete(self.empty_houses, pair)

	def removeAgent(self, agent):
		print(f"viewing agent at {agent.getX()},{agent.getY()}")
		agentX = agent.getX()
		agentY = agent.getY()
		agent.setX(-1)
		agent.setY(-1)
		self.matrix[agentX][agentY] = 0
		pair = (agentX, agentY)
		
		self.empty_houses.append(pair)
		print(self.empty_houses)
		

	def getAgent(self,x,y):
		return self.matrix[x][y]

	def getEmpty(self):
		return self.empty_houses

	def populate(self, agents):
		for x in range(self.width):
			for y in range(self.height):
				pair = (x,y)
				if pair in self.empty_houses:
					pass
				else:
					print(agents.pop())
					
					
	def moveAgent(self, agent, house):
		pair = (house[0], house[1])
				
		print(f"empty houses before : {self.empty_houses}")
		
		self.removeAgent(agent)
		
		agent.setPair(pair)
		
		self.addAgent(agent)
		
		print(f"empty houses after : {self.empty_houses}")
		


	def run(self):
		for x in range(self.width):
			for y in range(self.height):
				if self.matrix[x][y] == 0:
					pass
				else:
					agent = self.matrix[x][y]
					happy = agent.is_happy(self)
					
					if not happy:
						print(f"agent is unhappy at {x}, {y}")
						empty_places = self.getEmpty()
						
						empty_by_rank = []
						for house in empty_places: ###promote clustering by moving only to happy locations
							temp_agent = agent
							temp_agent.setX(house[0])
							temp_agent.setY(house[1])
							empty_by_rank.append(temp_agent.is_happy(self))
							
						
						iter = 0
						print(empty_places)
						print(empty_by_rank)
						for house in empty_places:
							if empty_by_rank[iter]:
								self.moveAgent(agent, house)
								break
							
							iter += 1
						
						
							
						return
				
		
					
	
def main():
	#game variables
	threshold_tol = 0.3
	width = 5
	height = 5
	empty = 0.11
	agent_prob= [0.5, 1] #acumulated
	niter = 500
	agents = []

	#create board
	board_a = Board(width,height,empty,niter)
	board_a.create()
	
	
	#populate board and keep agents in a list
	#agent creation loop
	
	empty_houses = board_a.getEmpty()
	print(empty_houses)
	
	totalagents = int(width*height*(1-empty))
	
	for i in range(totalagents):
		
		print(board_a.getEmpty())
		n = random.uniform(0,1)
		l = 0
		hasSpace = 0
		
		while l < len(agent_prob) and hasSpace == 0:
			if n <= agent_prob[l]:
				while hasSpace == 0:
					agentX = random.randint(0,width-1)
					agentY = random.randint(0,height-1)
					pair = (agentX, agentY)
					contents = board_a.getAgent(agentX,agentY)
					
					if contents == 0 and pair not in empty_houses:
						agent = Agent(l, threshold_tol, agentX, agentY)
						agents.append(agent)
						board_a.addAgent(agent)
						print(f"agent created at {pair} \n")

						hasSpace = 1
						
			
			l += 1

	#run simulation
# 	print('finished creating agents')
# 	for agent in agents:
# 		print(f"agent at {agent.getX(), agent.getY()}")
# 	print(board_a.getEmpty())
	#plot before
	#plotboard(board_a,agents,'Schelling Model with 2 colors: Initial State', 'file1_init.png')

	board_a.run()

	#plot after
	#plotboard(board_a,agents,'Schelling Model with 2 colors: Initial State', 'file1_final.png')

if __name__ == "__main__":
	main()
