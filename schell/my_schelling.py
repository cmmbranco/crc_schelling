#!/usr/bin/env python3

# CRC 2018/2019
# Group 98
# 71003, Carlos Branco
# 78690, Isaac Vargas

"""
An implementation of the Schelling's segregation model.
"""

# Python Modules
import argparse
import random
import math
import abc
import numpy as np
import matplotlib as plt

# Python Packages
import matplotlib.colors
import matplotlib.pyplot as plt
import pendulum



class AbstractAgentStrategy(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def rank_diff(self):
        """Required Method"""
        
class RacialStrategy(AbstractAgentStrategy):
    def rank_diff(self, agent):
        #print('Racial Strat')
        if self.race == agent.race:
            return 0
        else:
            return 1

class EconomicStrategy(AbstractAgentStrategy):
    def rank_diff(self, agent):
        #print('Economic Strat')
        if self.income == agent.income:
            return 0
        else:
            return 1

class AcademicStrategy(AbstractAgentStrategy):
    def rank_diff(self, agent):
        #print('Academic Strat')
        if self.academic == agent.academic:
            return 0
        else:
            return 1


class Agent:
    """
    Class Agent has 4 attributes:
        intolerance: float, level of intolerance of other Agents
        race: int, the defining characteristic of the Agent
        x, y: int, the coordinates of this Agent on the Board
    """

    def __init__(self, race, intolerance, x, y):
        self.intolerance = intolerance
        self.race = race
        self.x = x
        self.y = y
        
        if race == 0:
            self.behav = RacialStrategy
            self.income = 0
            self.academic = 0
        elif race == 1:
            self.behav = EconomicStrategy
            self.income = 1
            self.academic = 0
        elif race == 2:
            self.behav = AcademicStrategy
            self.income = 0
            self.academic = 1
        else:
            print('problems instantiating agent')


    def set_pair(self, pair):
        """
        Setter of the coordinates of the agent.

        :param pair: tuple of ints, with the new coordinates of the Agent
        :return: nothing
        """

        self.x = pair[0]
        self.y = pair[1]

    def rank_diff(self, agent):
        # can return some more complicated difference
        # implement via strategy pattern
        
        return self.behav.rank_diff(self,agent)
#         if agent.race == self.race:
#             return 0
#         else:
#             return 1

    def is_happy(self, neighbours):
        """
        Checks if the Agent is happy.

        :param neighbours: list of Agents, that are this Agent's neighbours
        :return: Boolean, happy or not
        """

        total = 0
        happy_with_neighbour = 0
        for neighbour in neighbours:
            total += 1
            if self.rank_diff(neighbour) == 0:
                happy_with_neighbour += 1

        return total == 0 or (happy_with_neighbour / total) >= self.intolerance



# Agent Behaviours




class Board:
    """
    Class Board has 6 attributes:
        width, height: int, the size of the Board
        empty_ratio: float, percentage (from 0 to 1) of empty houses on the Board
        empty_houses: list of tuples, where the tuple is a coordinate that is empty
        num_empty: int, the number of empty houses on the Board (size of the empty_houses list)
        matrix: 2 dimensional list, the Board itself where each entry is a house
            that if empty is None, if populated it's an Agent object
    """

    def __init__(self, width, height, empty_ratio):
        self.width = width
        self.height = height
        self.empty_ratio = empty_ratio
        self.empty_houses = []
        self.num_empty = int(math.ceil(width * height * empty_ratio))
        self.matrix = [[None for _x in range(width)] for _y in range(height)]

    def create_empty_houses(self):
        """
        Generates the list of empty houses.

        :return: nothing
        """

        for _i in range(self.num_empty):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            pair = (x, y)
            while pair in self.empty_houses:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                pair = (x, y)
            self.empty_houses.append(pair)

    def populate(self, agent_prob, intolerance_threshold):
        """
        Populates the Board with Agents.

        :param agent_prob: list of floats, cumulative probability,
            with the probability of creation of an Agent of that or previous race (list index)
        :param intolerance_threshold: list of floats,
            with the threshold of intolerance for each race (list index)
        :return: nothing
        """
        uniq_races = []
        self.create_empty_houses()
        agents = []
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self.empty_houses:
                    race_gen = random.uniform(0, 1)
                    race = next(aux[0] for aux in enumerate(agent_prob) if aux[1] >= race_gen)
                    uniq_races.append(race)
                    agent = Agent(race, intolerance_threshold[race], x, y)
                    agents.append(agent)
                    self.matrix[y][x] = agent
                    
        print(np.unique(uniq_races))

    def neighbours(self, agent):
        """
        Creates a list of the first level of neighbours of the given Agent.

        :param agent: an Agent object
        :return: list of Agents, that are this agent's neighbours
        """

        neighbours = []
        for y in (-1, 0, 1):
            for x in (-1, 0, 1):
                if (x != 0 or y != 0) \
                        and 0 <= agent.x + x < self.width and 0 <= agent.y + y < self.height:
                    neighbour = self.matrix[agent.y + y][agent.x + x]
                    if neighbour is not None:
                        neighbours.append(neighbour)
        return neighbours

    def move_agent(self, agent):
        """
        Moves an (unhappy) agent to an empty house and vacates the agent's house.

        :param agent: an Agent object
        :return: nothing
        """

        agent_house = (agent.x, agent.y)
        random_house = random.randint(0, self.num_empty - 1)
        empty_house = self.empty_houses.pop(random_house)
        self.empty_houses.append(agent_house)
        agent.x = empty_house[0]
        agent.y = empty_house[1]
        self.matrix[empty_house[1]][empty_house[0]] = agent
        self.matrix[agent_house[1]][agent_house[0]] = None

    def run(self, num_iterations):
        """
        Runs across the board checking if each Agent is unhappy.
        If an Agent is unhappy, move it to an empty house.
        Stops when every Agent is happy after running the allowed iterations.

        :param num_iterations: int, number of iterations to run this function
        :return: nothing
        """
        tot_iters = 0
        for iteration in range(num_iterations):
            print(iteration)
            unhappy = 0
            for y in range(self.height):
                for x in range(self.width):
                    agent = self.matrix[y][x]
                    if agent is not None:
                        neighbours = self.neighbours(agent)
                        happy = agent.is_happy(neighbours)
                        if not happy:
                            unhappy += 1
                            self.move_agent(agent)
            #print('There was {} unhappy agents at iteration {}.'.format(unhappy, iteration))
            if unhappy == 0:
                tot_iters += 1
                #print('Everyone was happy by iteration {}.'.format(iteration))
                break
        
            tot_iters += 1
        
        return tot_iters

    def plot(self, num_races, title, file_name):
        """
        Creates a plot with the current matrix and saves it in the current directory.

        :param num_races: int, to know how many colors to use
        :param title: string, to be the plot title
        :param file_name: string, to name the file
        :return: nothing
        """

        data = self.to_ints()
        available_colors = ['w', 'r', 'b', 'g', 'c', 'm', 'y', 'k']
        c_map = matplotlib.colors.ListedColormap(available_colors[:num_races + 1])
        plt.title(title)
        plt.imshow(data, cmap=c_map)
        plt.savefig(file_name)

    def to_ints(self):
        """
        Takes the current matrix and generates an alternative one with only ints instead of Agents.

        :return: 2 dimensional list of ints, the alternative matrix,
            that has -1 for empty houses and the race (int) of the Agent occupying it otherwise
        """

        int_matrix = [[-1 for _x in range(self.width)] for _y in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                if self.matrix[y][x] is not None:
                    int_matrix[y][x] = self.matrix[y][x].race
        return int_matrix


def main():
    """
    main function:
        reads the arguments from the command line and generates a board and then runs it.

    :return: nothing
    """
    sizes = [30,60,120,240,480]
    avg_times = []
    
    for i in range(len(sizes)):
        ##
        ##sequence for 3 agents is 
        ##RACE - ECONOMIC - ACADEMIC
        
        width = sizes[i]
        height = sizes[i]
        empty_ratio = 0.3
        agent_prob = [0.3, 0.6, 1]
        intolerance_threshold = [0.7,0.7,0.4]
        num_races = 3
        num_iterations = 5000
        
        board = Board(width, height, empty_ratio)
        print("POPULATING")
        board.populate(agent_prob, intolerance_threshold)
    
        board.plot(num_races,
                   'Schelling Model {}x{} with {} colors: Initial State'
                   .format(width, height, num_races),
                   'board_{}x{}_beginning.png'.format(width, height))
        
        print("RUNNING")
        time_0 = pendulum.now()
        iters = board.run(num_iterations)
        
        print(f"Total iterations were {iters}")
        time_1 = pendulum.now()
        delta = time_1 - time_0
        
        final_time = delta/iters
        
        avg_times.append(final_time)
    
        board.plot(num_races,
                   'Schelling Model {}x{} with {} colors: Final State'
                   .format(width, height, num_races),
                   'board_{}x{}_end.png'.format(width, height))
    

        print('This execution ran for {}'.format(delta.as_timedelta()))
        print(f'Average time per cycle was {final_time}')


    
    for i in range(len(sizes)):
        print(f"board of {sizes[i]}x{sizes[i]} took an average time of {avg_times[i]} per iteration")


    t = np.arange(0.00, 0.1, 0.1)
    
#     print(sizes)
#     print(avg_times)



if __name__ == "__main__":
    main()
