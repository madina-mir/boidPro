## 15-112 Term Project Proposal 
#### Video Demo video 
https://youtu.be/ZAk3_InR-3I?si=oa-UPNoOFjZRI8qC 
#### Link to proposal in google docs
https://docs.google.com/document/d/1d8c77tpWlHDaUj32hw10_Vy_PjAm29ZMr7o8wzsjhqQ/edit?usp=sharing 
# BOID algorithm - simulation of moving groups of animals
## Project Description
Boid algorithm was developed by Craig Reynolds in 1986, which simulates the flocking behaviour of birds and related groups of animals’ motion. While it has primarily been applied in animation and visual effects for movies, often with minimal interactivity, this project takes a different approach. The main motivation of me undertaking this project comes from a larger Research Project that aims to train a machine learning model for accurately counting animals moving in aggregations. One of the fundamental steps of the research is to accurately imitate behaviors of moving groups of animals. By implementing this simulation by adding extra interactivity and control for the user, I aim to come up with a simulation that is both unique in the field of boids simulation and also a meaningful contribution to my larger research project. 

## Competitive Analysis
There are numerous projects that have successfully implemented the Boid algorithm to simulate the movement of animal groups. While Craig Reynolds' original paper describes the algorithm in a generic manner, the main challenge lies in translating these rules into a working simulation. Many implementations exist in both 2D and 3D, showcasing realistic flocking behavior. One of the best 2D examples I found is this JavaScript-based simulation, which effectively demonstrates the algorithm's core principles.
My project differentiates itself by significantly increasing interactivity and complexity beyond traditional boid simulations. Unlike most existing implementations, which focus solely on the three fundamental flocking rules:
#### **Cohesion** – Boids move toward the perceived center of mass of nearby boids.
#### **Separation** – Boids avoid crowding by maintaining a safe distance from nearby boids.
#### **Alignment** – Boids align their velocity with the average velocity of their neighbors.
***
In addition to these, my simulation will incorporate **predator avoidance**, user control over the **number of boids**, real-time **boid creation** via mouse clicks, and interactive **obstacles** that mimic real-world constraints like trees. Additionally, this will be the first project to integrate these advanced behaviors using cmu_graphics, making it unique in both its scope and implementation framework.

***
### How the Buttons work?
R key stands for re-start 
You can type the number of boids that you want to draw.
All the buttons work using the mouse press.
You can open and close the menu using the mouse press, and all the 
features work using the mouse press. Some behaviors are mutually exclusive, 
meaning two of them can't be on at the same time as both rely on mouse press in their implementation. 
Arrow keys are used to move the Professors in the game mode. In general using the simulation is quite intuitive, and requires no knowledge. 

***
### Kind remarks
THIS IS NOT A GAME, but it has a small feature called special game. 
Images do collide, because they are using the boid rules being the child 
class of the boids. Given that I have used other rules, it would evade from the 
central topic of my project. 

***
### ACKNOWLEDGEMENT
I thank Craig Reynolds for observing 3 fundamental rules that guide moving groups of animals, and for coming up with this algorithm. Though his explanations are generic, it was a great intro for me to get started. I also thank Ben Eater, his youtube videos helped me better understand the boid algorithm. Lastly, I used a bit of computational geometry, specifically QuadTree, which was recommended by Professor Eduardo to reduce the complexity of the project, and I largely benefitted by the youtube channel called "Neat AI". 
Note: I am acknowledging the sources that I have learned the algorithms, though I give credit, no lines of code comes from the outside source in my project. 
