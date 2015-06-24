#imports - do later
from graphics import *

#the class
class Graph(self):

    self.data = {
        "Plankton": []
        "Carp": []
        "Fish": []
        }
    self.win_length, self.win_height = 1200, 800
    self.graph_length, self.graph_height = 0.75 * self.win_length, 0.75 * self.win_height
    
    def input_data(self, dataArray):
        self.data["Plankton"].append(dataArray[0])
        self.data["Carp"].append(dataArray[1])
        self.data["Fish"].append(dataArray[2])
    
    def display_graph(self):
        self.win = GraphWin("Population Graph", self.win_length, self.win_height)
        self.outline = Rectangle(Point(self.graph_length / 2, self.graph_height / 2), Point(self.win_length - (self.graph_length / 2), self.win_height - (self.graph_length / 2)))
        self.outline.draw(win)

        for i in self.data:
            
