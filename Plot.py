import networkx as nx

class Plot:
    def __init__(self, G):
        self.G = G
        self.infectedText = None
        self.recoveredText = None
        self.vaccinatedText = None
        self.deathsText = None

    def update_graph(self, layout, ax, day, color_map):
        # pos = nx.circular_layout(self.G)
        # nx.draw_networkx(self.G, pos)
        nx.draw_networkx_nodes(self.G, node_color=color_map, pos=layout)
        ax.set_title('Day {}'.format(day), fontweight="bold")

    def initialize_texts(self, ax):
        self.infectedText = ax.text(-1.05, 1.05, '', color='red')
        self.recoveredText = ax.text(-1.05, 1.00, '', color='green')
        self.vaccinatedText = ax.text(-1.05, 0.95, '', color='blue')
        self.deathsText = ax.text(-1.05, 0.90, '', color='black')

    def update_texts(self, infected_number, recovered_number, vaccinated_number, deaths_number):
        self.infectedText.set_text("Infected {}".format(infected_number))
        self.recoveredText.set_text("Recovered {}".format(recovered_number))
        self.vaccinatedText.set_text("Vaccinated {}".format(vaccinated_number))
        self.deathsText.set_text("Deaths {}".format(deaths_number))