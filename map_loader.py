from location import Location

class MapLoader:
    def __init__(self, filename):
        self.filename = filename
        self.maze = []
        self.characters = []
        self.gates = {
            'A': Location(0, 5),
            'B': Location(4, 0),
            'C': Location(12, 0),
            'D': Location(13, 5),
            'E': Location(4, 10)
        }
        
    def load_map(self):
        with open(self.filename, 'r') as file:
            for line in file:
                if line.strip() == "---":
                    break
                row = [int(x) for x in line.strip().split()]
                if row:
                    self.maze.append(row)
            
            for line in file:
                if line.strip():
                    char_info = line.strip().split(',')
                    if len(char_info) >= 2:
                        char_name = char_info[0].strip()
                        gate = char_info[1].strip()
                        self.characters.append((char_name, gate))
        
        return self.maze, self.characters, self.gates 