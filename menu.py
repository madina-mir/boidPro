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
        imagePath = ("images/onBtn.jpg" if \
                    self.state else "images/offBtn.jpg") 
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
        drawImage("images/forestGreen.JPG", 
            3*app.width//4, app.menuY, width=app.width//4, height=app.height,
            align='left-top')
        app.addBoid.drawButton()
        app.addObstacle.drawButton()
        app.predatorMode.drawButton()   
        app.specialGame.drawButton()    
    # draw the menu bar using image    
    drawImage("images/blackMenu.png", 
            app.menuX, app.menuY, width=app.menuWidth, height=app.menuHeight,
            align='left-top')  
    
    if app.predatorMode.state:
        # turn on the predator mode
        if app.pred:
            # lighting effect
            drawCircle(app.pred['x'], app.pred['y'], app.predatorSize*1.5, 
                    fill="White", opacity=20)
            # predator that I drew myself!
            drawImage("images/predator.png", 
                    app.pred['x'], app.pred['y'],
                    width = app.predatorSize, height = app.predatorSize,
                    rotateAngle = app.pred['d'], align="center")
        
    
    
    
def drawProfs(app):
    # choose the player label
    drawLabel("Choose the player!", app.width//2, app.height*0.2, 
              size = 30, fill = "white")
    
    # draw the Gianni Button
    drawImage("people/profGianni.png", app.gianniX, app.gianniY, 
              height = 200, width = 200, align = "center")
    drawLabel("Gianni the Great", app.gianniX, app.gianniY+100, 
              size = 25, fill = "white", font='times new roman')
    drawRect(app.gianniX, app.gianniY, app.gianniHeight, app.gianniWidth,
             fill = None, border = "blue", align = "center")
    
    # draw the Gianni Button
    drawImage("people/profEduardo.png", app.eduardoX, app.eduardoY, 
              height = 200, width = 200, align = "center")
    drawLabel("Eduardo the Great", app.eduardoX, app.eduardoY+100, 
              size = 25, fill = "white", font='times new roman')
    drawRect(app.eduardoX, app.eduardoY, app.eduardoHeight, app.eduardoWidth,
             fill = None, border = "blue", align = "center")