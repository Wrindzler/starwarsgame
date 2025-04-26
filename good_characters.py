from character import Character

class LukeSkywalker(Character):
    """
    Luke Skywalker Sınıfı - İyi karakter
    """
    def __init__(self, location):
        """
        Constructor - Luke Skywalker özelliklerini ayarlar
        """
        super().__init__("Luke Skywalker", "İyi", location)
        self.lives = 3
    
    def get_lives(self):
        """
        Can sayısını döndürür
        """
        return self.lives
    
    def set_lives(self, new_lives):
        """
        Can sayısını günceller
        """
        self.lives = new_lives
    
    def lose_life(self):
        """
        Yakalandığında 1 can kaybeder
        """
        self.lives -= 1
        return self.lives <= 0


class MasterYoda(Character):
    """
    Master Yoda Sınıfı - İyi karakter
    """
    def __init__(self, location):
        """
        Constructor - Master Yoda özelliklerini ayarlar
        """
        super().__init__("Master Yoda", "İyi", location)
        self.lives = 3
    
    def get_lives(self):
        """
        Can sayısını döndürür
        """
        return self.lives
    
    def set_lives(self, new_lives):
        """
        Can sayısını günceller
        """
        self.lives = new_lives
    
    def lose_life(self):
        """
        Yakalandığında canının yarısını kaybeder
        """
        self.lives = self.lives - 0.5
        return self.lives < 0.5
