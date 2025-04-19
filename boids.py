from cmu_graphics import *
import random 
import math
from wlecome import *
from ruleButtons import *
from menu import *
from quadTree import *
from specialGame import *

# HELPER FUNCTIONS
#__________________________________FIND_NEIGHBORS_______________________________
def neighbors(curBoid, quadtree, visualRange):
    # updated quadtree neighbor finder that loops only the area of its visual range
    
    # Create a box around the current boid
    # This is the area where we will search for nearby boids
    visionBox = Rectangle(
        curBoid.x - visualRange / 2,  # top-left x
        curBoid.y - visualRange / 2,  # top-left y
        visualRange,                  # width
        visualRange                   # height
    )
    # Ask the quadtree to return all points (boids) in that box
    nearbyPoints = quadtree.queryRange(visionBox)

    # Loop through the results and collect the actual boids 
    boidNeighbors = []
    for point in nearbyPoints:
        boid = point.data  # .data holds the actual boid object
        if boid != curBoid:  # don't include self
            boidNeighbors.append(boid)
    # Return the list of nearby boids, now it's super efficient!
    return boidNeighbors
#_______________________________APPLY_BOID_RULES________________________________
# apply rule of cohesion
def cohesion(boid, neighbors):
    if len(neighbors) == 0: # if there are no neighbors
        return (0, 0) # no change in velocity
    allX = []
    allY = []
    for neighbor in neighbors:
        allX.append(neighbor.x)
        allY.append(neighbor.y)
    avgX = sum(allX)/len(neighbors)
    avgY = sum(allY)/len(neighbors)
    changeDifference = (avgX - boid.x, avgY - boid.y)
    return changeDifference

# apply rule of alignment      
def alignment(boid, neighbors):
    if len(neighbors) == 0: 
        return (0, 0)
    allvx = []
    allvy = []
    for neighbor in neighbors:
        allvx.append(neighbor.vx)
        allvy.append(neighbor.vy)
    avgVx = sum(allvx)/len(neighbors)
    avgVy = sum(allvy)/len(neighbors)
    changeDifference = (avgVx - boid.vx, avgVy - boid.vy)
    return changeDifference

# apply rule of seperation
def separation(boid, neighbors, minDist):
    if len(neighbors) == 0:
        return (0, 0) 
    sepVector = [0, 0] 
    for neighbor in neighbors:
        dist = distance(boid.x, boid.y, neighbor.x, neighbor.y)
        if 0 < dist < minDist:  # Ensure it's within range
            sepVector[0] += (boid.x - neighbor.x) / dist  # Normalize
            sepVector[1] += (boid.y - neighbor.y) / dist  

    magnitude = (sepVector[0]**2 + sepVector[1]**2)**0.5
    if magnitude > 0:
        sepVector[0] /= magnitude
        sepVector[1] /= magnitude   
    return sepVector

# imitate separation behavior for avoiding the obstacles
def avoidObstacle(boid, obstacle, minDist):
    if len(obstacle) == 0:
        return (0, 0) 
    vector = [0, 0] 
    for obj in obstacle:
        dist = distance(boid.x, boid.y, obj[0], obj[1])
        if 0 < dist < minDist:  # Ensure it's within range
            vector[0] += (boid.x - obj[0]) / dist  # Normalize
            vector[1] += (boid.y - obj[1]) / dist  

    magnitude = (vector[0]**2 + vector[1]**2)**0.5
    if magnitude > 0:
        vector[0] /= magnitude
        vector[1] /= magnitude   
    return vector
    
# make the boids escape the predator
def avoidPredator (boid, predator, minDist):
    if predator == None:
        return (0, 0)
    dist = distance(boid.x, boid.y, predator['x'], predator['y'])
    vector = [0, 0]
    if 0 < dist < minDist:  # Ensure it's within range
        vector[0] += (boid.x - predator['x']) / dist  # Normalize
        vector[1] += (boid.y - predator['y']) / dist  
            
    magnitude = (vector[0]**2 + vector[1]**2)**0.5
    if magnitude > 0:
        vector[0] /= magnitude
        vector[1] /= magnitude      
    return vector
    
    
#draw boid polygons_____________________________________________________________ 
def drawBoid(app, boid):
     # Calculate rotation angle based on velocity
    """
        atan2(y, x) is used to calculate the angle of a vector (x, y) relative 
        to the x-axis, ensuring correct direction handling in all quadrants.
        It avoids division by zero and provides a full -180° to 180° range for 
        accurate boid rotation.
    """
    angle = math.degrees(math.atan2(boid.vy, boid.vx))
    # Define three points for the bird triangular shape
    tipX = boid.x + app.boidSize * 1.2 # Pointy front x
    tipY = boid.y  # Pointy front y
    leftX = boid.x - app.boidSize # Back left x
    leftY = boid.y - app.boidSize / 1.5 # Back left y
    rightX = boid.x - app.boidSize # Back right x
    rightY = boid.y + app.boidSize / 1.5  # Back right y
    drawPolygon(
        tipX, tipY,  # Tip of the triangle 
        leftX, leftY,  # Back left wing
        rightX, rightY,  # Back right wing
        fill = rgb(173, 216, 230),
        rotateAngle = angle)

    
#______________________________CLASS_BOIDS______________________________________
class Boids:
    # Initializes a boid with a position (x, y) and a velocity (vx, vy).
    # The velocity determines the direction and speed of movement.
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y 
        self.vx = vx 
        self.vy = vy 
    # Updates the boid's position by adding its velocity   
    def moveBoid(self, quadtree, visualRange, rule1, rule2, rule3, app):
        allNeighbors = neighbors(self, quadtree, visualRange)
        
        # apply the rules of cohesion
        if rule1: 
            cohesionImpact = cohesion(self, allNeighbors)
            self.vx += cohesionImpact[0] * 0.05 # slightly changes the vector in each frame toward the center mass
            self.vy += cohesionImpact[1] * 0.05
        
        # apply rules of alignment 
        if rule2:
            alignmentImpact = alignment(self, allNeighbors)
            self.vx += alignmentImpact[0] * 0.6
            self.vy += alignmentImpact[1] * 0.6
        
        # apply rules for separation
        if rule3:
            separationImpact = separation(self, allNeighbors, minDist = 30)
            self.vx += separationImpact[0] * 2.1
            self.vy += separationImpact[1] * 2.1
        
        # apply rule for avoiding obstacle 
        obstacleImpact = avoidObstacle(self, app.obstacle, 50)
        self.vx += obstacleImpact[0] * 4
        self.vy += obstacleImpact[1] * 4 # escape the obstacle with faster speed
        
        # apply rule for escaping the predator
        predatorImpact = avoidPredator(self, app.pred, 50)
        self.vx += predatorImpact[0] * 3
        self.vy += predatorImpact[1] * 3
        
        # limit the speed 
        maxSpeed = 15
        speed = (self.vx**2 + self.vy**2) ** 0.5 # calculate speed

        # If the boid's speed exceeds maxSpeed, scale velocity down 
        if speed > maxSpeed:
                # Normalize vx while maintaining direction
                self.vx = (self.vx / speed) * maxSpeed  
                # Normalize vy while maintaining direction
                self.vy = (self.vy / speed) * maxSpeed  
            
        self.x += self.vx
        self.y += self.vy 
        
    # each boid should avoid dissapearing from the canvas
    def avoidEdges(self, width, height):
        margin = 200 # margin by which boid starts to avoid
        turnFactor = 1 # factor by which boid makes the turn 
        if self.x < margin:
            self.vx += turnFactor
        if self.x > width - margin:
            self.vx -= turnFactor
        if self.y < margin:
            self.vy += turnFactor
        if self.y > height - margin:
            self.vy -= turnFactor
            
            
# child CLASS FOR PEOPLE
class People(Boids):
    def __init__(self, x, y, vx, vy, image):
        super().__init__(x, y, vx, vy)
        self.image = image
        
    def movePeople(self, quadtree, visualRange, rule1, rule2, rule3, app):
        return super().moveBoid(quadtree, visualRange, rule1, rule2, rule3, app)
    
    def avoidEdges(self, width, height):
        return super().avoidEdges(width, height)
    
    def draw(self):
        drawImage(self.image, self.x, self.y, width=100, height=100)
  
# manually drawing people
def addPeople(app):
    images = ["people/adam.png", "people/amen.png", 
              "people/anurag.png",  "people/belix.png",
              "people/mohammed.png", "people/salman.png", 
              "people/yasa.png"]
    for img in images:
        app.people.append(People(
            x = random.randint(0, app.width),
            y = random.randint(0, app.height),
            vx = random.uniform(-2, 2),
            vy = random.uniform(-2, 2),
            image = img
        ))
        
def drawPeople(app):
    for people in app.people:
        people.draw()

#______________________________________________________________________________
# Organization of variables assigned to onAppStart

def basicParameters(app):
    app.start = True
    app.color = rgb(90, 69, 167)
    
    # Boid rules 
    app.cohesion = True
    app.alignment = True 
    app.separation = True 
    # Boid's parameters
    app.boidNumber = 100
    app.boidSize = 6
    app.visualRange = 60
    """
    use the class Boids and create boidNumber of boids at random positions
    with initial velocity set between -2 to 2 so they go right/left/up/down
    """
    app.boids = []
    for boid in range(app.boidNumber):
        x = random.randint(0, app.width)
        y = random.randint(0, app.height)
        vx = random.uniform(-2, 2)
        vy = random.uniform(-2, 2)
        app.boids.append(Boids(x, y, vx, vy))
    
def ruleButtons(app):
    # Rule Botton coordinates 
    app.bottonY = app.height*0.9
    app.bottonWidth = app.width * 0.1
    app.bottonHeight = app.height * 0.05
    app.cohesionX = app.width * 0.1
    app.alignmentX = app.width * 0.3
    app.separationX = app.width * 0.5
    # passing variables to the class
    app.ruleButtons = BoidRuleButtons(app.width, app.height,
                        app.cohesionX, app.alignmentX, app.separationX,
                        app.bottonWidth, app.bottonY, app.bottonHeight)
    

def welcomePage(app):
    app.info = False # Opens instructions page
    app.enterNum = False # becomes true if user clicks the rect for user Input
    app.userInput = f"{app.boidNumber}"
    app.invalidNum = False # sets max and minimum enterable variable
    app.focus = False # shows when input can be modified
    # coordinates for the welcome page buttons 
    # create buttons using the class 
    app.boidInfo = WelcomeButtons(app.width/2, app.height * 0.38, 
                    app.width * 0.25, app.height * 0.1, "What is Boid?")
    app.inputButton = WelcomeButtons(app.width/2, app.height * 0.55, 
                    app.width * 0.25, app.height * 0.1, app.userInput)
    # start button 
    app.startButton = WelcomeButtons(app.width/2, app.height * 0.66, 
                    app.width * 0.25, app.height * 0.1, "START!")
    
def menuParameters(app):
    app.menuX = app.width - app.width * 0.05
    app.menuY = 0
    app.menuWidth = app.width * 0.05
    app.menuHeight =  app.height * 0.05
    app.menuOpen = False
    # creating buttons iside my menu 
    app.addBoid = MenuButton(app.height*0.2, "Add Boid", app)
    app.addObstacle = MenuButton(app.height*0.3, "Add Obstacle", app)
    app.obstacle = []
    # predator mode
    app.predatorMode = MenuButton(app.height*0.4, "Predator Mode", app)
    # predator Parameters
    app.predatorSize = 30
    app.pred = None
    # special game button
    app.specialGame = MenuButton(app.height*0.5, "Special Game", app)
    
 #____________________________onAppStart________________________________________    
def onAppStart(app):
    app.background = "black"
    app.width = 1400
    app.height = 800
    # fundamental variables for boid movement
    basicParameters(app)
    # Rule Botton coordinates 
    ruleButtons(app)
    # Welcome page variables
    welcomePage(app)
    # menu tab variables
    menuParameters(app)
    # Game paramters
    app.gameMode = False
    app.people = []
    app.gianni = False
    app.eduardo = False
    app.gianniX, app.gianniY = app.width//3, app.height//2
    app.gianniHeight, app.gianniWidth = app.width*0.2, app.height*0.35
    app.eduardoX, app.eduardoY = 2*app.width//3, app.height//2
    app.eduardoHeight, app.eduardoWidth =  app.width*0.2, app.height*0.35
    # to control how they are moving with arrows
    app.moveX, app.moveY = app.width//2, app.height//2
    app.profWidth, app.profHeight = 150, 150

# click R to reset!       
def reset(app):
    onAppStart(app) 
       
def onStep(app):
    # get the boids moving randomly
    # Build a new quadtree for this and each frame
    qt = Quadtree(Rectangle(0, 0, app.width, app.height), capacity=4)
    # Insert all boids into the quadtree based on current position
    for boid in app.boids:
        qt.insert(Point(boid.x, boid.y, data=boid)) 
        
        
    if not app.start and not app.gameMode:
        # move after welcome page is closed
        for boid in app.boids:
            # Move boid based on nearby boids using the quadtree
            boid.moveBoid(qt, app.visualRange, 
                app.cohesion, app.alignment, app.separation, app)
            boid.avoidEdges(app.width, app.height) 
    # runs people on the game mode
    if app.gameMode:
        qt = Quadtree(Rectangle(0, 0, app.width, app.height), capacity=4)
        for person in app.people: 
            qt.insert(Point(person.x, person.y, data=person))
        for person in app.people:
            person.movePeople(qt, app.visualRange,
                                app.cohesion, app.alignment, app.separation, app)
            person.avoidEdges(app.width, app.height)
        
       
    # Update the coordinates of the buttons in case of screen resize
    app.boidInfo = WelcomeButtons(app.width/2, app.height * 0.38, 
                    app.width * 0.25, app.height * 0.1, "What is Boid?") 
    app.inputButton = WelcomeButtons(app.width/2, app.height * 0.55, 
                    app.width * 0.25, app.height * 0.1, app.userInput)
    app.startButton = WelcomeButtons(app.width/2, app.height * 0.66, 
                    app.width * 0.25, app.height * 0.1, "START!")
    app.menuX = app.width - app.width * 0.05
    # update the list of obstacles in each frame
    app.obstacle = app.obstacle
         
def onMousePress(app, x, y):
    # start botton 
    if app.start:
            # Clicked "What is Boid?"
            if app.boidInfo.isInside(x, y):
                app.info = True
            # Clicked input box
            elif app.inputButton.isInside(x, y):
                app.focus = True
                app.enterNum = True # turn on focus
            else:
                app.enterNum = False  # Clicked outside input, disable typing
                app.focus = False  # remove focus
            # Clicked "START!"
            if app.startButton.isInside(x, y):
                if app.userInput.isdigit():
                    num = int(app.userInput)
                    if 0 <= num <= 500:
                        app.boidNumber = int(app.userInput)
                        app.boids = []
                        for _ in range(app.boidNumber):
                            bx = random.randint(0, app.width)
                            by = random.randint(0, app.height)
                            vx = random.uniform(-2, 2)
                            vy = random.uniform(-2, 2)
                            app.boids.append(Boids(bx, by, vx, vy))
                        app.start = False
                    else:
                        app.invalidNum = True 
                    
    # update true/false when rule buttons are clicked              
    if app.ruleButtons.cohesionClicked(x, y, app):
        app.cohesion = not app.cohesion
    if app.ruleButtons.alignmentClicked(x, y, app):
        app.alignment = not app.alignment
    if app.ruleButtons.separationClicked(x, y, app):
        app.separation = not app.separation
    # One mouse press boid generation
    if app.addBoid.state:
        newBoid = app.boids.append(Boids(x, y, random.uniform(-2, 2), 
                               random.uniform(-2, 2)))
        
    
    # when the menu bar is clicked, close and open the menu 
    if (app.menuX <= x <= app.menuX + app.menuWidth and
        app.menuY <= y <= app.menuY + app.menuHeight):
        app.menuOpen = not app.menuOpen
    
    # features in the menu
    if app.menuOpen:
        # mutually exclusive features for improved efficiency
        # add boids on Mouse click
        if app.addBoid.isOn(x, y):
            app.addBoid.state = True
            app.addObstacle.state = False
            app.predatorMode.state = False
        # add obstacles on mouse click
        elif app.addObstacle.isOn(x, y):
            app.addObstacle.state = True
            app.addBoid.state = False
            app.predatorMode.state = False
        # become a predator and scare the boids!
        elif app.predatorMode.isOn(x, y):
            app.predatorMode.state = True
            app.addBoid.state = False
            app.addObstacle.state = False
        elif app.specialGame.isOn(x, y):
            app.specialGame.state = not app.specialGame.state
            app.predatorMode.state = False
            app.addBoid.state = False
            app.addObstacle.state = False
            app.obstacle = []
           
         # switch mode to game  
        if app.specialGame.isOn(x, y):
            app.gameMode = not app.gameMode
            if app.gameMode:
                addPeople(app)
                
    # start the special game
    if app.gameMode:
        # clicked on prof Gianni 
        if (app.gianniX - app.gianniWidth/2 <= x <= app.gianniX + app.gianniWidth/2 and
            app.gianniY - app.gianniHeight/2 <= y <= app.gianniY + app.gianniHeight/2):
            app.gianni = True
        # clicked on prof Eduardo  
        if (app.eduardoX - app.eduardoWidth/2 <= x <= app.eduardoX + app.eduardoWidth/2 and
            app.eduardoY - app.eduardoHeight/2 <= y <= app.eduardoY + app.eduardoHeight/2):
            app.eduardo = True
    
    # avoid overdrawing the buttons with obstacles       
    if app.addObstacle.state and not (app.ruleButtons.cohesionClicked(x, y, app) or 
                                      app.ruleButtons.alignmentClicked(x, y, app) or
                                      app.ruleButtons.separationClicked(x, y, app)):
        app.obstacle.append((x, y))
    
    
def onKeyPress(app, key):
    if app.enterNum:
        if key.isdigit():
            app.userInput += key
            app.inputButton.label = app.userInput
        elif key == "backspace":
            app.userInput = app.userInput[:-1] 
            app.inputButton.label = app.userInput        
    if app.start:
        if app.info:
            if key == "backspace":
                app.info = False     
    # reset            
    if key == "r":
        reset(app)
        
def onMouseMove(app, x, y):
    # control the degree and movement of predator on mouse move
    if app.predatorMode.state:
        if app.pred != None:
            if (x != app.pred['x'] and app.pred['y'] != y):   #mouse pos changed    
                dx = x - app.pred['x']
                dy = y - app.pred['y']
                app.pred = {
                    'x': x,
                    'y': y,
                    'd': (math.degrees(math.atan2(dy, dx))+90)%360,
                }
        else:
            app.pred = {
                'x': x,
                'y': y,
                'd': 0,
            }

####

def onKeyHold(app, keys):
    step = 20
    if app.gianni or app.eduardo:
        if 'left' in keys:
            app.moveX -= step
        if 'right' in keys:
            app.moveX += step
        if 'up' in keys:
            app.moveY -= step
        if 'down' in keys:
            app.moveY += step
    
    # pop the people when the Professor catches
    i = 0
    while i < len(app.people):
        person = app.people[i]
        dx = app.moveX - person.x
        dy = app.moveY - person.y
        dist = (dx**2 + dy**2)**0.5
        if dist < 30:  # or use a collision radius you prefer
            app.people.pop(i)
        else:
            i += 1
    
              
def redrawAll(app):
    #  Loop through all boids and draw them as triangles 
    if not app.gameMode:
        for boid in app.boids:
            drawBoid(app, boid)  
    elif app.gameMode:
        if not app.gianni and not app.eduardo:
            drawProfs(app)
        if app.gianni or app.eduardo:
            moveProfs(app)
            drawPeople(app)
            
    # START PAGE 
    if app.start:
        drawWelcome(app)
        if app.info:
            drawInfoPage(app)
    else:
        menuBar(app)
         # draw the rule buttons 
        app.ruleButtons.draw(app) 
           
runApp()                