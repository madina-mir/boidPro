from cmu_graphics import *
import random 
import math
  
def menuBar(app):
    # menu bar 
    
    if app.menuOpen:
        drawImage("/Users/ziyodjanmirzataev/Desktop/boidPro/forestGreen.JPG", 
            3* app.width//4, app.menuY, width=app.width//4, height=app.height,
            align='left-top')
        
    drawImage("/Users/ziyodjanmirzataev/Desktop/boidPro/blackMenu.png", 
            app.menuX, app.menuY, width=app.menuWidth, height=app.menuHeight,
            align='left-top')  
   
         
