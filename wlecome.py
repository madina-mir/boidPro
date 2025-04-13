### WELCOME BUTTONS       
from cmu_graphics import *
import random 
def drawInfoPage(app):
    drawRect(app.width*0.2, 0, app.width * 0.6, app.height, 
                 fill = "white")
    drawLabel("Coming Soon...", app.width//2, app.height//3, size=50)
    drawLabel("press delete or backspace to go back", app.width//2, app.height//2, size=25)
    
class WelcomeButtons:
    def __init__(self, x, y, width, height, label):
        self.x = x
        self.y = y
        self.width = width 
        self.height = height 
        self.label = label
        self.focus = False 
    # method for drawing buttons with labels    
    def draw(self):
        drawRect(self.x, self.y, self.width, self.height, align="center",
                 fill=None, border = rgb(90, 69, 167) if self.focus else "white")
        drawLabel(self.label, self.x, self.y, 
                size = self.width*0.1, fill = "white", font='times new roman')
    # method to check if the button has been clicked   
    def isInside(self, x, y):
        return (self.x - self.width/2 <= x <= self.x + self.width/2 and
                self.y - self.height/2 <= y <= self.y + self.height/2)

    
def drawWelcome(app):
    # background coordinates
    drawRect(app.width*0.2, 0, app.width * 0.6, app.height, 
            fill = rgb(0, 33, 71))
    # welcome
    drawLabel("Welcome!", app.width/2, app.height*0.2, 
                size=app.width*0.05, font='times new roman', fill='white')
    drawLabel("This is a BOID simulation", app.width/2, app.height*0.28, 
                size=app.width*0.03, font='times new roman', fill='white')
    # what is boid button
    app.boidInfo.draw()
    # input button
    drawLabel("enter number between 0 and 200", app.width/2, app.height*0.46, 
                size=app.width*0.019, font='times new roman', fill='white')
    app.inputButton.draw()
    app.startButton.draw()  # start button
    if app.invalidNum:
        drawLabel("Enter valid number!", app.width/2, app.height*0.8, 
                  size = app.width*0.02, fill="red")