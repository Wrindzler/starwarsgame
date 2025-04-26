from location import Location
from abc import ABC, abstractmethod
import heapq
from collections import deque

class Character:
    """
    Temel Karakter Sınıfı - Tüm karakterlerin ortak özelliklerini içerir
    """
    def __init__(self, name, type, location):
        """
        Constructor - Karakter özelliklerini ayarlar
        """
        self.name = name
        self.type = type
        self.location = location
    
    def get_name(self):
        """
        Karakterin adını döndürür
        """
        return self.name
    
    def set_name(self, new_name):
        """
        Karakterin adını günceller
        """
        self.name = new_name
    
    def get_type(self):
        """
        Karakterin türünü döndürür
        """
        return self.type
    
    def set_type(self, new_type):
        """
        Karakterin türünü günceller
        """
        self.type = new_type
    
    def get_location(self):
        """
        Karakterin konumunu döndürür
        """
        return self.location
    
    def set_location(self, new_location):
        """
        Karakterin konumunu günceller
        """
        self.location = new_location
    
    def shortest_path(self, maze, target_location):
        return []

class GoodCharacter(Character):
    def __init__(self, name, location, lives=3.0):
        super().__init__(name, "Good", location)
        self.lives = lives
    
    def get_lives(self):
        return self.lives
    
    def set_lives(self, lives):
        self.lives = lives

class LukeSkywalker(GoodCharacter):
    def __init__(self, location):
        super().__init__("Luke Skywalker", location)
    
    def lose_life(self):
        self.lives -= 1
        return self.lives <= 0

class MasterYoda(GoodCharacter):
    def __init__(self, location):
        super().__init__("Master Yoda", location)
    
    def lose_life(self):
        self.lives -= 0.5
        return self.lives <= 0

class BadCharacter(Character, ABC):
    def __init__(self, name, location):
        super().__init__(name, "Bad", location)
    
    @abstractmethod
    def shortest_path(self, maze, target_location):
        pass

class DarthVader(BadCharacter):
    def __init__(self, location):
        super().__init__("Darth Vader", location)
    
    def shortest_path(self, maze, target_location):
        rows, cols = len(maze), len(maze[0])
        visited = set()
        queue = [(0, self.location, [])]
        
        while queue:
            dist, current, path = heapq.heappop(queue)
            
            if current.get_x() == target_location.get_x() and current.get_y() == target_location.get_y():
                return path + [current]
            
            if (current.get_x(), current.get_y()) in visited:
                continue
            
            visited.add((current.get_x(), current.get_y()))
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x = current.get_x() + dx
                new_y = current.get_y() + dy
                
                if 0 <= new_x < cols and 0 <= new_y < rows:
                    new_loc = Location(new_x, new_y)
                    if (new_x, new_y) not in visited:
                        manhattan_dist = abs(new_x - target_location.get_x()) + abs(new_y - target_location.get_y())
                        heapq.heappush(queue, (manhattan_dist, new_loc, path + [current]))
        
        return []

class KyloRen(BadCharacter):
    def __init__(self, location):
        super().__init__("Kylo Ren", location)
    
    def shortest_path(self, maze, target_location):
        rows, cols = len(maze), len(maze[0])
        visited = set()
        queue = deque([(self.location, [])])
        
        while queue:
            current, path = queue.popleft()
            
            if current.get_x() == target_location.get_x() and current.get_y() == target_location.get_y():
                return path + [current]
            
            if (current.get_x(), current.get_y()) in visited:
                continue
            
            visited.add((current.get_x(), current.get_y()))
            
            for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                new_x = current.get_x() + dx
                new_y = current.get_y() + dy
                
                if 0 <= new_x < cols and 0 <= new_y < rows and maze[new_y][new_x] == 1:
                    mid_x = current.get_x() + dx//2
                    mid_y = current.get_y() + dy//2
                    if maze[mid_y][mid_x] == 1:
                        new_loc = Location(new_x, new_y)
                        if (new_x, new_y) not in visited:
                            queue.appendleft((new_loc, path + [current]))
                            continue
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x = current.get_x() + dx
                new_y = current.get_y() + dy
                
                if 0 <= new_x < cols and 0 <= new_y < rows and maze[new_y][new_x] == 1:
                    new_loc = Location(new_x, new_y)
                    if (new_x, new_y) not in visited:
                        queue.append((new_loc, path + [current]))
        
        return []

class Stormtrooper(BadCharacter):
    def __init__(self, location):
        super().__init__("Stormtrooper", location)
    
    def shortest_path(self, maze, target_location):
        rows, cols = len(maze), len(maze[0])
        current_x = self.location.get_x()
        current_y = self.location.get_y()
        
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        path = [self.location]
        
        best_move = None
        best_distance = float('inf')
        
        for dx, dy in moves:
            new_x = current_x + dx
            new_y = current_y + dy
            
            if (0 <= new_x < cols and 
                0 <= new_y < rows and 
                maze[new_y][new_x] == 1):
                distance = abs(new_x - target_location.get_x()) + abs(new_y - target_location.get_y())
                if distance < best_distance:
                    best_distance = distance
                    best_move = (new_x, new_y)
        
        if best_move:
            path.append(Location(best_move[0], best_move[1]))
        
        return path
