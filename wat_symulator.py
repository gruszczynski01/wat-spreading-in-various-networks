import random
import matplotlib.pyplot as plt
import networkx as nx
from networkx.generators.random_graphs import erdos_renyi_graph
from networkx.generators.random_graphs import watts_strogatz_graph
from matplotlib import animation
from Plot import Plot

SUSCEPTIBLE = []
INFECTED = []
RECOVERED = []
DEATH = []
VACINNATED = []

INITIAL_INFECTED = 0.1
PROBABILITY_OF_INFECTION = 0.2
DEATH_PROBABILITY = 0.03

STEPS_TO_RECOVERED = 7

VACINNATED_PER_DAY = 1

# TODO: dorobic rozne miary centralnosci
RANDOM_VACINNATED_STRATEGY = 'RANDOM_VACINNATED_STRATEGY'
NODE_DEGREE_VACINNATED_STRATEGY = 'NODE_DEGREE_VACINNATED_STRATEGY'

CHOOSEN_VACINNATED_STRATEGY = NODE_DEGREE_VACINNATED_STRATEGY

recovery = []

NODE = 200


def move_to_susceptible(node):
    SUSCEPTIBLE.append(node)


def remove_from_susceptible(node):
    SUSCEPTIBLE.remove(node)


def move_to_infected(node):
    INFECTED.append(node)


def remove_from_infected(node):
    INFECTED.remove(node)


def move_to_recovered(node):
    RECOVERED.append(node)


def remove_from_recovered(node):
    RECOVERED.remove(node)


def move_to_death(node):
    DEATH.append(node)


def remove_from_recovery(node):
    rec_to_delete = -1
    for rec in recovery:
        if rec[1] == node:
            rec_to_delete = [rec]
            break
    if rec_to_delete != -1:
        for element in rec_to_delete:
            recovery.remove(element)


def move_to_vacinnated(node):
    VACINNATED.append(node)


def update_colors():
    color_map = []
    for i in range(0, NODE):
        if i in SUSCEPTIBLE:
            color_map.append("yellow")
        if i in INFECTED:
            color_map.append("red")
        if i in RECOVERED:
            color_map.append("green")
        if i in DEATH:
            color_map.append("black")
        if i in VACINNATED:
            color_map.append("blue")
    return color_map


def decision(probability):
    return random.random() < probability


def sim_step(frame, layout, ax, day):
    day = DAY
    if CHOOSEN_VACINNATED_STRATEGY == RANDOM_VACINNATED_STRATEGY:
        VACINNATED_THAT_DAY = VACINNATED_PER_DAY
        if VACINNATED_PER_DAY > len(SUSCEPTIBLE):
            VACINNATED_THAT_DAY = len(SUSCEPTIBLE)
        for i in range(0, VACINNATED_PER_DAY):
            index_to_vacinnated = random.randint(0, VACINNATED_THAT_DAY)
            node_to_vacinnated = SUSCEPTIBLE[index_to_vacinnated]
            remove_from_susceptible(node_to_vacinnated)
            move_to_vacinnated(node_to_vacinnated)
            print("Node: " + str(node_to_vacinnated) + " has been vacinnated")

    if CHOOSEN_VACINNATED_STRATEGY == NODE_DEGREE_VACINNATED_STRATEGY:
        VACINNATED_THAT_DAY = VACINNATED_PER_DAY
        if VACINNATED_PER_DAY > len(SUSCEPTIBLE):
            VACINNATED_THAT_DAY = len(SUSCEPTIBLE)
        if len(SUSCEPTIBLE) > 0:
            for i in range(0, VACINNATED_PER_DAY):
                node_to_vacinnated = ""
                while node_to_vacinnated == "":
                    node_to_vacinnated_candidate = verex_sorted_by_degree.pop(0)[0]
                    if node_to_vacinnated_candidate in SUSCEPTIBLE:
                        node_to_vacinnated = node_to_vacinnated_candidate

                print(node_to_vacinnated)
                remove_from_susceptible(node_to_vacinnated)
                move_to_vacinnated(node_to_vacinnated)
                print("Node: " + str(node_to_vacinnated) + " has been vacinnated")

    # infected undirectional
    for edge in G.edges():
        # print(edge)
        if edge[0] in INFECTED and edge[1] in SUSCEPTIBLE and decision(PROBABILITY_OF_INFECTION):
            print("Node: " + str(edge[1]) + " has been infected")
            remove_from_susceptible(edge[1])
            move_to_infected(edge[1])
            recovery.append(tuple((day + STEPS_TO_RECOVERED, edge[1])))
            if decision(DEATH_PROBABILITY):
                remove_from_infected(edge[1])
                move_to_death(edge[1])
                remove_from_recovery(edge[1])

        if edge[1] in INFECTED and edge[0] in SUSCEPTIBLE and decision(PROBABILITY_OF_INFECTION):
            print("Node: " + str(edge[0]) + " has been infected")
            remove_from_susceptible(edge[0])
            move_to_infected(edge[0])
            recovery.append(tuple((day + STEPS_TO_RECOVERED, edge[0])))
            if decision(DEATH_PROBABILITY):
                remove_from_infected(edge[0])
                move_to_death(edge[0])
                remove_from_recovery(edge[0])

        # recovered
    for rec in recovery:
        if rec[0] == day:
            remove_from_infected(rec[1])
            move_to_recovered(rec[1])
            remove_from_recovery(rec)
            print("Node: " + str(edge[0]) + " has been recovered")

    update_layout(layout, ax)

    # for node in INFECTED:
    #     if decision(DEATH_PROBABILITY):
    #         remove_from_infected(node)
    #         move_to_death(node)
    #         remove_from_recovery(node)


def update_layout(layout, ax):
    global DAY
    color_map = update_colors()
    plot.update_layout(layout, ax, DAY, color_map)
    plot.updateText(len(INFECTED), len(RECOVERED), len(VACINNATED), len(DEATH))
    DAY += 1


def on_click(event):
    if anim.running:
        anim.event_source.stop()
    else:
        anim.event_source.start()
    anim.running ^= True


anim = None


def simple_animation():
    fig, ax = plt.subplots(figsize=(10, 10))

    layout = nx.circular_layout(G)
    nx.draw_networkx(G, layout)
    plot.initializeTexts(ax)

    global anim
    anim = animation.FuncAnimation(fig, sim_step, frames=10, fargs=(layout, ax, 0), interval=1000)
    anim.running = True

    cid = fig.canvas.mpl_connect('button_press_event', on_click)

    plt.show()


DAY = 0
ended_on = 0
results = []

# fig, ax = plt.subplots(figsize=(8, 8))

for test in range(0, 1):
    SUSCEPTIBLE = []
    INFECTED = []
    RECOVERED = []
    DEATH = []

    # G = watts_strogatz_graph(NODE, 5, 0.2)
    G = nx.scale_free_graph(NODE)
    plot = Plot(G)

    verex_sorted_by_degree = sorted(G.degree, key=lambda x: x[1], reverse=True)
    print("verex_sorted_by_degree:")
    print(verex_sorted_by_degree)

    for i in range(0, NODE):
        move_to_susceptible(i)

    for i in range(0, NODE):
        if decision(INITIAL_INFECTED):
            print("Node: " + str(i) + " has been infected")
            remove_from_susceptible(i)
            move_to_infected(i)
            recovery.append(tuple((0 + STEPS_TO_RECOVERED, i)))
            if decision(DEATH_PROBABILITY):
                remove_from_infected(i)
                move_to_death(i)
                remove_from_recovery(i)

    simple_animation()

sum = 0
for i in results:
    print(i)
    sum = sum + i

print(len(results))
print(sum)

print("avg")
print(sum / 1)
