#imports - do later
from graphics import *

#the class
class Graph():

    data = {
        "Plankton": [],
        "Fish": [],
        "Carp": []
        }
    win_length, win_height = 1200, 800
    graph_length, graph_height = 0.75 * win_length, 0.75 * win_height
    start_x, start_y = (win_length - graph_length) / 2, (win_height - graph_height) / 2
    raw_data = []

    def input_data(self, dataArray):
        self.data["Plankton"].append(dataArray[0])
        self.data["Fish"].append(dataArray[1])
        self.data["Carp"].append(dataArray[2])

    def display_graph(self):
        self.win = GraphWin("Population over Time", self.win_length, self.win_height)
        print("Window")
        self.outline = Rectangle(Point(self.start_x, self.start_y), Point(self.win_length - self.start_x, self.win_height - self.start_y))
        print("Theorized Rectangle")
        self.outline.draw(self.win)
        print("Materialized rectangle!")
        self.highest_y = self.find_max(self.read_data())
        print("I can read")
        print(self.highest_y)
        self.highest_x, self.my_data = len(self.raw_data), self.read_data()
        print(self.highest_x)
        #print(self.data["Plankton"], "\n", "\n", self.data["Fish"], "\n", "\n", self.data["Carp"], "\n", "\n", self.raw_data)
        self.scale_x = self.highest_x / self.graph_length
        print(self.scale_x)
        self.scale_y = self.highest_y / self.graph_height
        print(self.scale_y)
        self.x, self.y = self.start_x, self.start_y
        i = 0
        while self.x < self.start_x + self.graph_length:
            self.high = self.find_total(self.my_data[i])
            print(i)
            
            self.rect = Rectangle(Point(int(self.x), self.graph_height * (1 - (self.my_data[i][0] / self.high))), Point(int(self.x + 1), self.start_y))
            self.rect.setFill(color_rgb(0, 255, 0))
            self.rect.draw(self.win)
            print(self.x)
            print(self.graph_height * (1 - (self.my_data[i][0] / self.high)))

            self.rect = Rectangle(Point(int(self.x), self.graph_height * (1 - (self.my_data[i][1] / self.high))), Point(int(self.x + 1), self.graph_height * (1 - (self.my_data[i][0] / self.high))))
            self.rect.setFill(color_rgb(0, 0, 255))
            self.rect.draw(self.win)
            print(self.graph_height * (1 - (self.my_data[i][0] / self.high)))

            self.rect = Rectangle(Point(int(self.x), self.graph_height * (1 - (self.my_data[i][2] / self.high))), Point(int(self.x + 1), self.graph_height * (1 - (self.my_data[i][1] / self.high))))
            self.rect.setFill(color_rgb(255, 0, 0))
            self.rect.draw(self.win)
            print(self.graph_height * (1 - (self.my_data[i][0] / self.high)))

            self.x = self.x + self.scale_x
            i = int(self.x / self.scale_x)

    def read_data(self):
        self.plankton_data, self.fish_data, self.carp_data = [], [], []
        for i in self.data["Plankton"]:
            self.plankton_data.append(i)
        for i in self.data["Fish"]:
            self.fish_data.append(i)
        for i in self.data["Carp"]:
            self.carp_data.append(i)
        for i in range(len(self.plankton_data)):
            self.raw_data.append([self.plankton_data[i], self.fish_data[i], self.carp_data[i]])
        return self.raw_data

    def find_total(self, array):
        return array[0] + array[1] + array[2]
    
    def find_max(self, array):
        total = 0
        for i in range(len(array)):
            temp = 0
            for j in range(3):
                temp += array[i][j]
            if total < temp:
                total = temp
        if total > 0:
            return total
        return 0
