import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation


class Plot:
    def __init__(self, G):
        self.G = G
        self.infectedText = None
        self.recoveredText = None
        self.vaccinatedText = None
        self.deathsText = None

    def update_layout(self, layout, ax, day, color_map):
        # pos = nx.circular_layout(self.G)
        # nx.draw_networkx(self.G, pos)
        nx.draw_networkx_nodes(self.G, node_color=color_map, pos=layout)
        ax.set_title('Day {}'.format(day), fontweight="bold")

    def update_text(self, time_text, infected_number):
        time_text.set_text("Infected {}".format(infected_number))

    def initializeTexts(self, ax):
        self.infectedText = ax.text(-1, -0.8, '', color='red')
        self.recoveredText = ax.text(-1, -0.9, '', color='green')
        self.vaccinatedText = ax.text(-1, -1.0, '', color='blue')
        self.deathsText = ax.text(-1, -1.1, '', color='black')

    def updateText(self, infected_number, recovered_number, vaccinated_number, deaths_number):
        self.infectedText.set_text("Infected {}".format(infected_number))
        self.recoveredText.set_text("Recovered {}".format(recovered_number))
        self.vaccinatedText.set_text("Vaccinated {}".format(vaccinated_number))
        self.deathsText.set_text("Deaths {}".format(deaths_number))