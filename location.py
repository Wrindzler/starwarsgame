class Location:
    """
    Lokasyon Sınıfı - Karakterlerin konum bilgisini tutar
    """
    def __init__(self, x, y):
        """
        Constructor - Başlangıç konumunu ayarlar
        """
        self.x = x
        self.y = y
    
    def get_x(self):
        """
        X koordinatını döndürür
        """
        return self.x
    
    def get_y(self):
        """
        Y koordinatını döndürür
        """
        return self.y
    
    def set_x(self, x):
        """
        X koordinatını günceller
        """
        self.x = x
    
    def set_y(self, y):
        """
        Y koordinatını günceller
        """
        self.y = y
        
    def __eq__(self, other):
        """
        İki konumun eşit olup olmadığını kontrol eder
        """
        if not isinstance(other, Location):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __str__(self):
        """
        Konum bilgisini string olarak döndürür
        """
        return f"({self.x}, {self.y})"
