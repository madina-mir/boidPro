from cmu_graphics import *
import random 

#__________________________Rules_BUTTON_HELPERS____________________________
# this class controls 3 boid rules that appear on the screen
class BoidRuleButtons:
    def __init__(self, x, y, cohesionX, alignmentX, separationX,
                 bottonWidth, bottonY, bottonHeight):
        self.x = x
        self.y = y
        self.cohesionX = cohesionX
        self.alignmentX = alignmentX
        self.separationX = separationX
        self.bottonWidth = bottonWidth
        self.bottonY = bottonY
        self.bottonHeight = bottonHeight
    
    def cohesionClicked(self, x, y, app):
        bottonY = app.height*0.9
        return (self.cohesionX <= x <= self.cohesionX + self.bottonWidth 
                and bottonY <= y <= bottonY + self.bottonHeight)

    def alignmentClicked(self, x, y, app):
        bottonY = app.height*0.9
        return (self.alignmentX <= x <= self.alignmentX + self.bottonWidth
                and bottonY <= y <= bottonY + self.bottonHeight)

    def separationClicked(self, x, y, app):
        bottonY = app.height*0.9
        return (self.separationX <= x <= self.separationX + self.bottonWidth
                and bottonY <= y <= bottonY + self.bottonHeight)
        
    def draw(self, app):
        bottonY = app.height*0.9
        bottonWidth = app.width * 0.1
        bottonHeight = app.height * 0.05
        cohesionX = app.width * 0.1
        alignmentX = app.width * 0.3
        separationX = app.width * 0.5
        # Cohesion
        drawRect(cohesionX,  bottonY,  bottonWidth,
                  bottonHeight, border="green" if app.cohesion else "red")
        drawLabel("Cohesion",  cohesionX +  bottonWidth / 2,
                   bottonY +  bottonHeight / 2, fill="white")
        
        # Alignment
        drawRect( alignmentX,  bottonY,  bottonWidth, 
                  bottonHeight, border="green" if app.alignment else "red")
        drawLabel("Alignment",  alignmentX +  bottonWidth / 2,
                   bottonY +  bottonHeight / 2, fill="white")
        
        # Separation
        drawRect( separationX,  bottonY,  bottonWidth, 
                  bottonHeight, border="green" if app.separation else "red")
        drawLabel("Separation",  separationX +  bottonWidth / 2,
                   bottonY +  bottonHeight / 2, fill="white")


     
     