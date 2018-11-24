#!/usr/bin/env python3

# CRC 2018/2019
# Group 98
# 71003, Carlos Branco
# 78690, Isaac Vargas

"""
An implementation of the Schelling's segregation model.
"""

# Python Modules
import abc
import argparse
import math
import random

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
        # print('Racial Strategy')
        if self.race == agent.race:
            return 0
        else:
            return 1


class EconomicStrategy(AbstractAgentStrategy):
    def rank_diff(self, agent):
        if self.income == agent.income:
            return 0
        else:
            return 1


class AcademicStrategy(AbstractAgentStrategy):
    def rank_diff(self, agent):
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
            self.behaviour = RacialStrategy
            self.income = 0
            self.academic = 0
        elif race == 1:
            self.behaviour = EconomicStrategy
            self.income = 1
            self.academic = 0
        elif race == 2:
            self.behaviour = AcademicStrategy
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
        return self.behaviour.rank_diff(self, agent)

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

        self.create_empty_houses()
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self.empty_houses:
                    race_gen = random.uniform(0, 1)
                    race = next(aux[0] for aux in enumerate(agent_prob) if aux[1] >= race_gen)
                    agent = Agent(race, intolerance_threshold[race], x, y)
                    self.matrix[y][x] = agent

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

        total_iterations = 0
        for iteration in range(num_iterations):
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
            total_iterations += 1
            if unhappy == 0:
                break
        
        return total_iterations

    def calculate_happiness(self):
        happy = 0
        total = 0
        for y in range(self.height):
            for x in range(self.width):
                agent = self.matrix[y][x]
                if agent is not None:
                    total += 1
                    neighbours = self.neighbours(agent)
                    if agent.is_happy(neighbours):
                        happy += 1

        return round(happy / total, 2)

    def calculate_segregation_happiness(self):
        happy = 0
        neighbours_similarity = []
        for y in range(self.height):
            for x in range(self.width):
                agent = self.matrix[y][x]
                if agent is not None:
                    neighbours = self.neighbours(agent)
                    total = 0
                    happy_with_neighbour = 0
                    for neighbour in neighbours:
                        total += 1
                        if agent.rank_diff(neighbour) == 0:
                            happy_with_neighbour += 1

                    if total == 0:
                        neighbours_similarity.append(total)
                        happy += 1
                    else:
                        neighbours_similarity.append(happy_with_neighbour / total)
                        if happy_with_neighbour / total >= agent.intolerance:
                            happy += 1

        return round(sum(neighbours_similarity) / len(neighbours_similarity) * 100, 2), \
            round(happy / len(neighbours_similarity) * 100, 2)

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

    parser = argparse.ArgumentParser(description='Simulate Schelling\'s segregation model.')
    parser.add_argument('-wi', '--width', dest='width',
                        default=100, nargs='?', type=int,
                        help='board\'s width')
    parser.add_argument('-he', '--height', dest='height',
                        default=100, nargs='?', type=int,
                        help='board\'s height')
    parser.add_argument('-e', '--empty_ratio', dest='empty_ratio',
                        default=0.10, nargs='?', type=float,
                        help='board\'s percentage of empty houses (zero to one)')
    parser.add_argument('-r', '--num_races', dest='num_races',
                        default=2, nargs='?', type=int,
                        help='number of races')
    parser.add_argument('-a', '--agents', dest='agent_prob',
                        default=[0.5, 1], nargs='*', type=float,
                        help='list of size equal to the number of races'
                             'where it\'s the accumulative probability'
                             'of spawning an agent of that race (their index)')
    parser.add_argument('-t', '--intolerance', dest='intolerance_threshold',
                        default=[0.5, 0.5], nargs='*', type=float,
                        help='list of size equal to the number of races'
                             'where it\'s the intolerance threshold'
                             'of an agent of that race (their index)')
    parser.add_argument('-i', '--num_iterations', dest='num_iterations',
                        default=500, nargs='?', type=int,
                        help='number of iterations')

    args = parser.parse_args()

    time_initialization_start = pendulum.now()
    board = Board(args.width, args.height, args.empty_ratio)
    board.populate(args.agent_prob, args.intolerance_threshold)
    time_initialization_end = pendulum.now()

    initialization_delta = time_initialization_end - time_initialization_start
    print('The initialization time was {}'.format(initialization_delta.as_timedelta()))

    segregation, happiness = board.calculate_segregation_happiness()
    board.plot(args.num_races,
               'Initial State: {}% segregation, {}% happiness'
               .format(segregation, happiness),
               'board_{}x{}_beginning.png'.format(args.width, args.height))

    time_run_start = pendulum.now()
    total_iterations = board.run(args.num_iterations)
    time_run_end = pendulum.now()

    run_delta = time_run_end - time_run_start
    print('The run time was {}'.format(run_delta.as_timedelta()))

    time_cycle = run_delta.as_timedelta() / total_iterations
    print('Average time per run iteration was {}'.format(time_cycle))

    segregation, happiness = board.calculate_segregation_happiness()
    board.plot(args.num_races,
               'Final State: {}% segregation, {}% happiness'
               .format(segregation, happiness),
               'board_{}x{}_end.png'.format(args.width, args.height))


if __name__ == "__main__":
    time_main_start = pendulum.now()
    main()
    time_main_end = pendulum.now()
    main_delta = time_main_end - time_main_start
    print('The total execution time was {}'.format(main_delta.as_timedelta()))
