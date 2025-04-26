from map_loader import MapLoader
from character import *
from location import Location
from good_characters import LukeSkywalker, MasterYoda
from bad_characters import DarthVader, KyloRen, Stormtrooper
import os
import random

class GameManager:
    """
    Oyun Yöneticisi Sınıfı - Oyun mantığını yönetir
    """
    def __init__(self, map_file):
        """
        Constructor - Oyun yöneticisini başlatır
        """
        self.map_loader = MapLoader(map_file)
        self.maze, self.characters_info, self.gates = self.map_loader.load_map()
        self.good_character = None
        self.bad_characters = []
        self.goal_location = Location(13, 9)
        self.start_location = Location(6, 5)
        self.game_over = False
        self.win = False
        
        for char_name, gate in self.characters_info:
            gate_loc = self.gates[gate]
            if char_name == "Darth Vader":
                self.bad_characters.append(DarthVader(gate_loc))
            elif char_name == "Kylo Ren":
                self.bad_characters.append(KyloRen(gate_loc))
            elif char_name == "Stormtrooper":
                self.bad_characters.append(Stormtrooper(gate_loc))
    
    def select_character(self, character_type):
        """
        Oyuncunun seçtiği karakteri ayarlar
        """
        if character_type == "Luke":
            self.good_character = LukeSkywalker(self.start_location)
        else:
            self.good_character = MasterYoda(self.start_location)
    
    def reset_game(self):
        self.good_character.set_location(self.start_location)
        self.game_over = False
        self.win = False
        
        for char_name, gate in self.characters_info:
            gate_loc = self.gates[gate]
            for bad_char in self.bad_characters:
                if bad_char.get_name() == char_name:
                    bad_char.set_location(gate_loc)
    
    def move_player(self, direction):
        """
        Oyuncuyu belirtilen yönde hareket ettirir
        """
        if not self.good_character or self.is_game_over() or self.is_win():
            return False
        
        current_loc = self.good_character.get_location()
        new_x, new_y = current_loc.get_x(), current_loc.get_y()
        
        if direction == "up":
            new_y -= 1
        elif direction == "down":
            new_y += 1
        elif direction == "left":
            new_x -= 1
        elif direction == "right":
            new_x += 1
        
        if (0 <= new_x < len(self.maze[0]) and 
            0 <= new_y < len(self.maze) and 
            self.maze[new_y][new_x] == 1):
            
            new_loc = Location(new_x, new_y)
            self.good_character.set_location(new_loc)
            
            for bad_char in self.bad_characters:
                if (bad_char.get_location().get_x() == new_x and 
                    bad_char.get_location().get_y() == new_y):
                    if self.good_character.lose_life():
                        self.game_over = True
                    self.reset_positions()
                    return True
            
            if new_x == self.goal_location.get_x() and new_y == self.goal_location.get_y():
                self.win = True
                return True
            
            self.move_bad_characters()
            return True
        
        return False
    
    def move_bad_characters(self):
        """
        Kötü karakterleri hareket ettirir ve yakalama kontrolü yapar
        """
        player_loc = self.good_character.get_location()
        
        for bad_char in self.bad_characters:
            yeni_konum = bad_char.takip_et(player_loc, self.maze)
            if yeni_konum:
                bad_char.set_location(yeni_konum)
                
                if (bad_char.get_location().get_x() == player_loc.get_x() and 
                    bad_char.get_location().get_y() == player_loc.get_y()):
                    if self.good_character.lose_life():
                        self.game_over = True
                    self.reset_positions()
                    return
    
    def reset_positions(self):
        """
        Oyuncu ve kötü karakterleri başlangıç konumlarına gönderir
        """
        self.good_character.set_location(self.start_location)
        
        available_gates = list(self.gates.values())
        
        for bad_character in self.bad_characters:
            if available_gates:
                random_index = random.randint(0, len(available_gates) - 1)
                gate_loc = available_gates.pop(random_index)
                bad_character.set_location(gate_loc)
    
    def get_maze(self):
        """
        Oyun haritasını döndürür
        """
        return self.maze
    
    def get_good_character(self):
        """
        İyi karakteri döndürür
        """
        return self.good_character
    
    def get_bad_characters(self):
        """
        Kötü karakterleri döndürür
        """
        return self.bad_characters
    
    def get_goal_location(self):
        """
        Hedef konumunu döndürür
        """
        return self.goal_location
    
    def is_game_over(self):
        """
        Oyunun bitip bitmediğini döndürür
        """
        return self.game_over
    
    def is_win(self):
        """
        Oyunun kazanılıp kazanılmadığını döndürür
        """
        return self.win
    
    def get_shortest_path_info(self):
        """
        Her kötü karakterin oyuncuya olan en kısa yol uzunluğunu hesaplar
        """
        path_info = []
        player_loc = self.good_character.get_location()
        
        for bad_char in self.bad_characters:
            path = bad_char.find_shortest_path(self.maze, player_loc)
            if path:
                path_info.append((bad_char.get_name(), len(path) - 1, path))
        
        return path_info if path_info else None
