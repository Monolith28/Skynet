import random

class Vertex:
    def __init__(self, name: str):
        self.name = name
        self.edges = {}
    
    def add_weight(self, target, weight: int):
        #a weight of zero implies no edge (you aren't moving)
        if weight > 0:
            self.edges[target] = weight
    
    def __str__(self):
        print_string = ""
        for edge in self.edges:
            print_string += f" -> {edge.name} ({self.edges[edge]}), "
        return f"{self.name}: " + print_string


class Network:

    places = ['Assembly Hall', 'Gymnasium', 'Offices', 'Technical Block', 'Classrooms','Staff Room']

    weights = {
        'Assembly Hall': [0,3,5,10,6,4], 
        'Gymnasium': [3,0,8,9,10,5], 
        'Offices': [5,8,0,5,7,5], 
        'Technical Block': [10,9,5,0,2,4], 
        'Classrooms': [6,10,7,2,0,3],
        'Staff Room': [4,5,5,4,3,0]
}
    def __init__(self):
        self.vertices = {}

    #vertices are stored in a dictionary, retreivable by name
    def populate_vertices(self):
        for place in self.places:
            self.vertices[place] = Vertex(place)
    
    #adds all the weights
    def populate_weights(self):
        for place in self.weights:
            weightlist = self.weights[place]
            for i in range(len(weightlist)):
                self.vertices[place].add_weight(self.vertices[self.places[i]], weightlist[i])

    def take_path(self, start: str, end: str):
        #if this threshold is exeeded, stop looking down this road
        paths = []
        path = []
        path_length = 0
        current = self.vertices[start]
        end = self.vertices[end]

        path.append(current)

        while path_length < 26:
            next = self.next(current)
            path_length += current.edges[next]
            path.append(next)
            current = next

            #min length for solution
            if len(path) > len(self.places) and current == end:
                if self.check_finished(path):
                    return path_length, path
                else:
                    return None

    def next(self, start: Vertex):
        return random.choice(list(start.edges.keys()))
    
    #Returns true if every location visited at least once, false if not
    def check_finished(self, path):
        finished = True
        for place in self.vertices:
            vertex = self.vertices[place]
            if vertex not in path:
                finished = False
                return False
        return finished

    




    def print_network(self):
        for location in self.vertices:
            print(self.vertices[location])

    def print_path(self, path: list):
        print_string = ""
        print_paragraph = ""
        for vertex in path[1]:
            print_string += f"{vertex.name} -> "
        return f"{path[0]} min:  {print_string[:-4]}"

        

        
    def __str__(self):
        self.print_network()
        return ""


def main():
    network = Network()
    network.populate_vertices()
    network.populate_weights()

    #print(network)
    paths = {}

    iterations = 1000000
    for i in range(iterations):
        print(f"Calculating {round(i/iterations*100)}%")
        mypath = network.take_path('Offices', 'Offices')
        if mypath is None:
            continue
        if mypath[0] not in paths:
            paths[mypath[0]] = [mypath]
        else:
            if mypath not in paths[mypath[0]]:
                paths[mypath[0]].append(mypath)
    
    #sort the dictionary
    paths = dict(sorted(paths.items()))


    with open('shortpaths.txt', 'w') as new_file:
        for time in paths.keys():
            if time < 26:
                for path in paths[time]:
                    new_file.write(f"{network.print_path(path)}\n")
                    print(network.print_path(path))


main()
        



