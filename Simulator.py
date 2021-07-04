import random
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import animation
from Plot import Plot
import numpy as np


class Simulator:
    def __init__(self):

        self.NODE = 70

        self.SMALL_WORLD_GRAPH = 'SMALL_WORLD_GRAPH'
        self.SCALE_FREE_GRAPH = 'SCALE_FREE_GRAPH'
        self.REGULAR_GRAPH = 'REGULAR_GRAPH'
        self.RANDOM_GRAPH = 'RANDOM_GRAPH'

        self.CHOSEN_GRAPH_TYPE = self.RANDOM_GRAPH

        if self.CHOSEN_GRAPH_TYPE == self.SMALL_WORLD_GRAPH:
            G = nx.watts_strogatz_graph(self.NODE, 5, 0.2)
        if self.CHOSEN_GRAPH_TYPE == self.SCALE_FREE_GRAPH:
            G = nx.scale_free_graph(self.NODE)
        if self.CHOSEN_GRAPH_TYPE == self.REGULAR_GRAPH:
            G = nx.random_regular_graph(6, self.NODE)
        if self.CHOSEN_GRAPH_TYPE == self.RANDOM_GRAPH:
            G = nx.gnp_random_graph(self.NODE, 0.05)

        # G = watts_strogatz_graph(NODE, 5, 0.2) #small world

        # random_regular_graph(d, n[, seed])

        # gnp_random_graph(n, p, seed=None, directed=False)

        plot = Plot(G)

        self.plot = plot
        self.anim = None
        self.anim2 = None

        self.susceptible = []
        self.infected = []
        self.recovered = []
        self.dead = []
        self.vaccinated = []
        self.recovery_calendar = []
        self.vertex_sorted_by_degree = []

        # TODO: dorobic rozne miary centralnosci
        self.RANDOM_VACINNATED_STRATEGY = 'RANDOM_VACINNATED_STRATEGY'
        self.NODE_DEGREE_VACINNATED_STRATEGY = 'NODE_DEGREE_VACINNATED_STRATEGY'

        self.INITIAL_INFECTED = 0.1
        self.PROBABILITY_OF_INFECTION = 0.2
        self.DEATH_PROBABILITY = 0.03
        self.STEPS_TO_RECOVERED = 7
        self.VACINNATED_PER_DAY = 1
        self.x = []
        self.y_infected = []
        self.y_recovered = []
        self.y_vaccinated = []
        self.y_dead = []

        self.DAY = 0
        self.CHOOSEN_VACINNATED_STRATEGY = self.RANDOM_VACINNATED_STRATEGY

        self.vertex_sorted_by_degree = sorted(self.plot.G.degree, key=lambda x: x[1], reverse=True)

        self.move_all_to_susceptible()

        self.move_initial_infected()

    def move_to_susceptible(self, node):
        self.susceptible.append(node)

    def remove_from_susceptible(self, node):
        self.susceptible.remove(node)

    def move_to_infected(self, node):
        self.infected.append(node)

    def remove_from_infected(self, node):
        self.infected.remove(node)

    def move_to_recovered(self, node):
        self.recovered.append(node)

    def remove_from_recovered(self, node):
        self.recovered.remove(node)

    def move_to_death(self, node):
        self.dead.append(node)

    def remove_from_recovery(self, node):
        rec_to_delete = -1
        for rec in self.recovery_calendar:
            if rec[1] == node:
                rec_to_delete = [rec]
                break
        if rec_to_delete != -1:
            for element in rec_to_delete:
                self.recovery_calendar.remove(element)

    def move_to_vacinnated(self, node):
        self.vaccinated.append(node)

    def move_all_to_susceptible(self):
        for i in range(0, self.NODE):
            self.move_to_susceptible(i)

    def move_initial_infected(self):
        for i in range(0, self.NODE):
            if self.decision(self.INITIAL_INFECTED):
                print("Node: " + str(i) + " has been infected")
                self.remove_from_susceptible(i)
                self.move_to_infected(i)
                self.recovery_calendar.append(tuple((0 + self.STEPS_TO_RECOVERED, i)))
                if self.decision(self.DEATH_PROBABILITY):
                    self.remove_from_infected(i)
                    self.move_to_death(i)
                    self.remove_from_recovery(i)

    def update_colors(self):
        color_map = []
        for i in range(0, self.NODE):
            if i in self.susceptible:
                color_map.append("yellow")
            if i in self.infected:
                color_map.append("red")
            if i in self.recovered:
                color_map.append("green")
            if i in self.dead:
                color_map.append("black")
            if i in self.vaccinated:
                color_map.append("blue")
        return color_map

    def decision(self, probability):
        return random.random() < probability

    def sim_step(self, frame, layout, ax):
        if self.CHOOSEN_VACINNATED_STRATEGY == self.RANDOM_VACINNATED_STRATEGY:
            VACINNATED_THAT_DAY = self.VACINNATED_PER_DAY
            if self.VACINNATED_PER_DAY > len(self.susceptible):
                VACINNATED_THAT_DAY = len(self.susceptible)
            for i in range(0, self.VACINNATED_PER_DAY):
                index_to_vacinnated = random.randint(0, VACINNATED_THAT_DAY)
                node_to_vacinnated = self.susceptible[index_to_vacinnated]
                self.remove_from_susceptible(node_to_vacinnated)
                self.move_to_vacinnated(node_to_vacinnated)
                print("Node: " + str(node_to_vacinnated) + " has been vacinnated")

        if self.CHOOSEN_VACINNATED_STRATEGY == self.NODE_DEGREE_VACINNATED_STRATEGY:
            VACINNATED_THAT_DAY = self.VACINNATED_PER_DAY
            if self.VACINNATED_PER_DAY > len(self.susceptible):
                VACINNATED_THAT_DAY = len(self.susceptible)
            if len(self.susceptible) > 0:
                for i in range(0, self.VACINNATED_PER_DAY):
                    node_to_vacinnated = ""
                    while node_to_vacinnated == "":
                        node_to_vacinnated_candidate = self.vertex_sorted_by_degree.pop(0)[0]
                        if node_to_vacinnated_candidate in self.susceptible:
                            node_to_vacinnated = node_to_vacinnated_candidate

                    print(node_to_vacinnated)
                    self.remove_from_susceptible(node_to_vacinnated)
                    self.move_to_vacinnated(node_to_vacinnated)
                    print("Node: " + str(node_to_vacinnated) + " has been vacinnated")

        # infected undirectional
        for edge in self.plot.G.edges():
            # print(edge)
            if edge[0] in self.infected and edge[1] in self.susceptible and self.decision(
                    self.PROBABILITY_OF_INFECTION):
                print("Node: " + str(edge[1]) + " has been infected")
                self.remove_from_susceptible(edge[1])
                self.move_to_infected(edge[1])
                self.recovery_calendar.append(tuple((self.DAY + self.STEPS_TO_RECOVERED, edge[1])))
                if self.decision(self.DEATH_PROBABILITY):
                    self.remove_from_infected(edge[1])
                    self.move_to_death(edge[1])
                    self.remove_from_recovery(edge[1])

            if edge[1] in self.infected and edge[0] in self.susceptible and self.decision(
                    self.PROBABILITY_OF_INFECTION):
                print("Node: " + str(edge[0]) + " has been infected")
                self.remove_from_susceptible(edge[0])
                self.move_to_infected(edge[0])
                self.recovery_calendar.append(tuple((self.DAY + self.STEPS_TO_RECOVERED, edge[0])))
                if self.decision(self.DEATH_PROBABILITY):
                    self.remove_from_infected(edge[0])
                    self.move_to_death(edge[0])
                    self.remove_from_recovery(edge[0])

            # recovered
        for rec in self.recovery_calendar:
            if rec[0] == self.DAY:
                self.remove_from_infected(rec[1])
                self.move_to_recovered(rec[1])
                self.remove_from_recovery(rec)
                print("Node: " + str(edge[0]) + " has been recovered")

        self.update_layout(layout, ax)

    # for node in INFECTED:
    #     if decision(DEATH_PROBABILITY):
    #         remove_from_infected(node)
    #         move_to_death(node)
    #         remove_from_recovery(node)

    def update_layout(self, layout, ax):
        color_map = self.update_colors()
        self.plot.update_graph(layout, ax, self.DAY, color_map)
        self.plot.update_texts(len(self.infected), len(self.recovered), len(self.vaccinated), len(self.dead))
        self.DAY += 1

    def animate(self, frame, ax):
        self.x.append(self.DAY)
        self.y_infected.append(len(self.infected))
        self.y_recovered.append(len(self.recovered))
        self.y_vaccinated.append(len(self.vaccinated))
        self.y_dead.append(len(self.dead))
        ax.set_ylim([0, 100])

        ax.plot(self.x, self.y_infected, color="red")
        ax.plot(self.x, self.y_recovered, color="green")
        ax.plot(self.x, self.y_vaccinated, color="blue")
        ax.plot(self.x, self.y_dead, color="black")

    def on_click(self, event):
        if self.anim.running:
            self.anim.event_source.stop()
        else:
            self.anim.event_source.start()
        self.anim.running ^= True

    def simple_animation(self):
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 10))

        layout = nx.circular_layout(self.plot.G)
        nx.draw_networkx(self.plot.G, layout)
        self.plot.initialize_texts(ax2)

        self.anim2 = animation.FuncAnimation(fig, self.animate, fargs=(ax1,), interval=1000)
        self.anim = animation.FuncAnimation(fig, self.sim_step, fargs=(layout, ax1), interval=1000)

        self.anim.running = True

        cid = fig.canvas.mpl_connect('button_press_event', self.on_click)

        plt.show()