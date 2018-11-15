#!/usr/bin/env python3

# CRC 2018/2019
# Group 98
# 71003, Carlos Branco
# 78690, Isaac Vargas

"""
An implementation of the Schelling's segregation model.
"""

# Python Modules
import random
import math

# Python Packages
import matplotlib.colors as colors
import matplotlib.pyplot as plt


class Agent:
    def __init__(self, race, tolerance, x, y):
        self.tolerance = tolerance
        self.race = race
        self.x = x
        self.y = y

    def set_pair(self, pair):
        self.x = pair[0]
        self.y = pair[1]

    def rank_diff(self, agent):
        # can return some more complicated difference
        # implement via strategy pattern
        if agent.race == self.race:
            return 0
        else:
            return 1

    def is_happy(self, neighbours):
        total = 0
        same_race = 0
        for neighbour in neighbours:
            total += 1
            if self.rank_diff(neighbour) == 0:
                same_race += 1

        if total == 0 or (same_race / total) >= self.tolerance:
            return True
        else:
            return False


class Board:
    def __init__(self, width, height, empty_ratio):
        self.width = width
        self.height = height
        self.empty_ratio = empty_ratio
        self.empty_houses = []
        self.num_empty = int(math.ceil(width * height * empty_ratio))
        self.matrix = [[None for _x in range(width)] for _y in range(height)]

    def create_empty_houses(self):
        for i in range(self.num_empty):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            pair = (x, y)
            while pair in self.empty_houses:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                pair = (x, y)
            self.empty_houses.append(pair)

    def populate(self, agent_prob, threshold_tolerance):
        self.create_empty_houses()
        agents = []
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self.empty_houses:
                    race_generator = random.uniform(0, 1)
                    race = next(aux[0] for aux in enumerate(agent_prob) if aux[1] >= race_generator)
                    agent = Agent(race, threshold_tolerance[race], x, y)
                    agents.append(agent)
                    self.matrix[y][x] = agent
        return agents

    def neighbours(self, agent):
        neighbours = []
        for y in (-1, 0, 1):
            for x in (-1, 0, 1):
                if (x != 0 or y != 0) and 0 <= agent.x + x < self.width and 0 <= agent.y + y < self.height:
                    neighbour = self.matrix[agent.y + y][agent.x + x]
                    if neighbour is not None:
                        neighbours.append(neighbour)
        return neighbours

    def move_agent(self, agent):
        agent_house = (agent.x, agent.y)
        random_house = random.randint(0, self.num_empty - 1)
        empty_house = self.empty_houses.pop(random_house)
        self.empty_houses.append(agent_house)
        agent.x = empty_house[0]
        agent.y = empty_house[1]
        self.matrix[empty_house[1]][empty_house[0]] = agent
        self.matrix[agent_house[1]][agent_house[0]] = None

    def run(self, num_iterations):
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
                            # empty_by_rank = []
                            # for house in self.empty_houses :  # promote clustering by moving only to happy locations
                            #    temp_agent = agent
                            #    temp_agent.set_x(house[0])
                            #    temp_agent.set_y(house[1])
                            #    empty_by_rank.append(temp_agent.is_happy(self))
            print('There was {} unhappy agents at the beginning of iteration {}.'.format(unhappy, iteration))
            if unhappy == 0:
                print('Everyone was happy by iteration {}.'.format(iteration))
                break

    def plot(self, num_races, title, file_name):
        data = self.to_ints()
        available_colors = ['w', 'r', 'b', 'g', 'c', 'm', 'y', 'k']
        c_map = colors.ListedColormap(available_colors[:num_races + 1])
        plt.title(title)
        plt.imshow(data, cmap=c_map)
        plt.savefig(file_name)

    def to_ints(self):  # auxiliary method
        int_matrix = [[-1 for _x in range(self.width)] for _y in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                if self.matrix[y][x] is not None:
                    int_matrix[y][x] = self.matrix[y][x].race
        return int_matrix


def main():
    # board variables
    width = 300
    height = 300
    empty_ratio = 0.11

    # agent variables
    num_races = 2
    agent_prob = [0.5, 1]   # accumulative probability
    threshold_tolerance = [0.3, 0.3]    # not accumulative probability

    # simulation variables
    num_iterations = 20

    # create the board and populate it
    board = Board(width, height, empty_ratio)
    board.populate(agent_prob, threshold_tolerance)

    # plot the board before running the simulation and after
    board.plot(num_races, 'Schelling Model with {} colors: Initial State'.format(num_races), 'board_initial.png')
    board.run(num_iterations)
    board.plot(num_races, 'Schelling Model with {} colors: Final State'.format(num_races), 'board_final.png')


if __name__ == "__main__":
    main()
