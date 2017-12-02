import pygame

class cat(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.
    
    def __init__(self,x,y):
        # Call the parent class (Sprite) constructor
        super(cat,self).__init__()
        
        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
	self.image = pygame.image.load("game/cat.png").convert_alpha()
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.x=x*48
        self.rect.y=y*48

    def coords(self):
        return self.rect.x/48,self.rect.y/48
