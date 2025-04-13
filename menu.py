from cmu_graphics import *
import random 
import math

def drawMenu(app):
    # menu bar 
        # Menu bar (top right)
    drawRect(app.width - app.width * 0.05, 0,
             app.width * 0.05, app.height * 0.05,
             fill=app.color, border="white")

    # "Hamburger" icon lines
    drawLine(app.width - app.width * 0.05 + app.width * 0.005,
             app.height * 0.05 * 0.3,
             app.width - app.width * 0.005,
             app.height * 0.05 * 0.3,
             fill="white")

    drawLine(app.width - app.width * 0.05 + app.width * 0.005,
             app.height * 0.05 * 0.6,
             app.width - app.width * 0.005,
             app.height * 0.05 * 0.6,
             fill="white")
     
