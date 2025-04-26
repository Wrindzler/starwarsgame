from character import Character
from location import Location
import heapq
from collections import deque

class BadCharacter(Character):
    def __init__(self, name, location):
        super().__init__(name, "Bad", location)
        self.step_size = 1
        self.can_break_walls = False
    
    def get_step_size(self):
        return self.step_size
    
    def can_break_wall(self):
        return self.can_break_walls
    
    def can_move_to(self, maze, x, y):
        if x < 0 or x >= len(maze[0]) or y < 0 or y >= len(maze):
            return False
        return self.can_break_walls or maze[y][x] == 1

    def find_shortest_path(self, maze, target_location):
        queue = deque([(self.location, [self.location])])
        visited = {(self.location.get_x(), self.location.get_y())}
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while queue:
            current_loc, path = queue.popleft()
            
            if (current_loc.get_x() == target_location.get_x() and 
                current_loc.get_y() == target_location.get_y()):
                return path
            
            for dx, dy in moves:
                new_x = current_loc.get_x() + dx
                new_y = current_loc.get_y() + dy
                
                if ((new_x, new_y) not in visited and 
                    self.can_move_to(maze, new_x, new_y)):
                    new_loc = Location(new_x, new_y)
                    visited.add((new_x, new_y))
                    new_path = path + [new_loc]
                    queue.append((new_loc, new_path))
        
        return [self.location]

    def takip_et(self, target_location, maze):
        path = self.find_shortest_path(maze, target_location)
        if len(path) > 1:
            return path[1]
        return None

class DarthVader(BadCharacter):
    def __init__(self, location):
        super().__init__("Darth Vader", location)
        self.can_break_walls = True
        self.step_size = 1

    def find_shortest_path(self, maze, target_location):
        rows, cols = len(maze), len(maze[0])
        start = (self.location.get_x(), self.location.get_y())
        goal = (target_location.get_x(), target_location.get_y())
        
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}
        
        while frontier:
            current = heapq.heappop(frontier)[1]
            
            if current == goal:
                break
                
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_x = current[0] + dx
                next_y = current[1] + dy
                next_pos = (next_x, next_y)
                
                if not (0 <= next_x < cols and 0 <= next_y < rows):
                    continue
                    
                new_cost = cost_so_far[current] + (2 if maze[next_y][next_x] == 0 else 1)
                
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + abs(goal[0] - next_x) + abs(goal[1] - next_y)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current
        
        if goal not in came_from:
            return [self.location]
            
        path = []
        current = goal
        while current is not None:
            path.append(Location(current[0], current[1]))
            current = came_from[current]
        path.reverse()
        return path

    def takip_et(self, target_location, maze):
        path = self.find_shortest_path(maze, target_location)
        if len(path) > 1:
            return path[1]
        return None

class KyloRen(BadCharacter):
    def __init__(self, location):
        super().__init__("Kylo Ren", location)
        self.step_size = 2
        self.can_break_walls = False

    def takip_et(self, target_location, maze):
        path = self.find_shortest_path(maze, target_location)
        if len(path) <= 1:
            return None
            
        first_step = path[1]
        current_x = self.location.get_x()
        current_y = self.location.get_y()
        dx = first_step.get_x() - current_x
        dy = first_step.get_y() - current_y
        
        if len(path) > 2:
            second_step = path[2]
            if dx != 0:
                if (second_step.get_y() == current_y and
                    abs(second_step.get_x() - current_x) == 2):
                    return second_step
            elif dy != 0:
                if (second_step.get_x() == current_x and
                    abs(second_step.get_y() - current_y) == 2):
                    return second_step
        
        return path[1]

class Stormtrooper(BadCharacter):
    def __init__(self, location):
        super().__init__("Stormtrooper", location)
        self.step_size = 1
        self.can_break_walls = False

    def takip_et(self, target_location, maze):
        path = self.find_shortest_path(maze, target_location)
        if len(path) > 1:
            return path[1]
        return None
