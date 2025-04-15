from cmu_graphics import *
import random 
import math


# this class is for controlling the buttons inside the menu
class MenuButton:
    def __init__(self, y, label, app, state=False):
        self.y = y 
        self.state = state 
        self.label = label
        self.x =  3*app.width//4
        self.width = app.width//4
        self.height = app.height * 0.08 
        
    
    # checks if on/off is clicked and returns true/false
    def isOn(self, mouseX, mouseY):
        return (self.x <= mouseX <= self.x + self.width and
                self.y <= mouseY <= self.y + self.height)

    # from True to False and vice versa
    def toggle(self):
        self.state = not self.state

    def drawButton(self):
        drawRect(self.x, self.y, self.width, self.height, fill="white")
        drawLabel(self.label, self.x + self.width*0.3, self.y+self.height//2, 
                  fill="black", size=self.height*0.3)
        imagePath = ("/Users/ziyodjanmirzataev/Desktop/boidPro/onBtn.jpg" if \
                    self.state else "/Users/ziyodjanmirzataev/Desktop/boidPro/offBtn.jpg") 
        drawImage(imagePath,
                  self.x + self.width - self.width * 0.2,
                  self.y + self.height * 0.1,
                  width=self.height * 0.9,
                  height=self.height * 0.7,
                  align='left-top') 
        
  
def menuBar(app):
    # obstacle is drawn on mouse press
    for obstacle in app.obstacle:
        drawCircle(obstacle[0], obstacle[1], 10, fill="red")
        
    # menu bar 
    # background for when menu is open
    
    if app.menuOpen:
        drawImage("/Users/ziyodjanmirzataev/Desktop/boidPro/forestGreen.JPG", 
            3*app.width//4, app.menuY, width=app.width//4, height=app.height,
            align='left-top')
        app.addBoid.drawButton()
        app.addObstacle.drawButton()
        app.predatorMode.drawButton()       
    # draw the menu bar using image    
    drawImage("/Users/ziyodjanmirzataev/Desktop/boidPro/blackMenu.png", 
            app.menuX, app.menuY, width=app.menuWidth, height=app.menuHeight,
            align='left-top')  
    
    if app.predatorMode.state:
        # turn on the predator mode
        if app.pred:
            drawCircle(app.pred['x'], app.pred['y'], app.predatorSize*1.5, 
                    fill="White", opacity=20)
            drawImage("/Users/ziyodjanmirzataev/Desktop/boidPro/predator.png", 
                    app.pred['x'], app.pred['y'],
                    width = app.predatorSize, height = app.predatorSize,
                    rotateAngle = app.pred['d'], align="center")
        
    
    
    
    
    