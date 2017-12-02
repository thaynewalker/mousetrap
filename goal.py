import pygame
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class goal(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.
    
    def __init__(self,x,y):
        # Call the parent class (Sprite) constructor
        super(goal,self).__init__()
        
        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        #self.image = pygame.Surface([width, height])
	self.image = pygame.image.load("game/stink.png").convert_alpha()
        #self.image.fill(WHITE)
        #self.image.set_colorkey(WHITE)
 
        # Draw the car (a rectangle!)
        #pygame.draw.rect(self.image, (10,10,10), [0, 0, width, height])
        
        # Instead we could load a proper pciture of a car...
        # self.image = pygame.image.load("car.png").convert_alpha()
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.x=x*48
        self.rect.y=y*48

    def coords(self):
        return self.rect.x/48,self.rect.y/48
