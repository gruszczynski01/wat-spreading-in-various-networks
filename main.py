import networkx as nx
from Plot import Plot
from Simulator import Simulator


for test in range(0, 1):

    # G = watts_strogatz_graph(NODE, 5, 0.2)


    simulator = Simulator()
    # simulator.plot = plot



    # for i in range(0, simulator.NODE):
    #     simulator.move_to_susceptible(i)
    #
    # for i in range(0, simulator.NODE):
    #     if simulator.decision(simulator.INITIAL_INFECTED):
    #         print("Node: " + str(i) + " has been infected")
    #         simulator.remove_from_susceptible(i)
    #         simulator.move_to_infected(i)
    #         simulator.recovery_calendar.append(tuple((0 + simulator.STEPS_TO_RECOVERED, i)))
    #         if simulator.decision(simulator.DEATH_PROBABILITY):
    #             simulator.remove_from_infected(i)
    #             simulator.move_to_death(i)
    #             simulator.remove_from_recovery(i)

    simulator.simple_animation()

