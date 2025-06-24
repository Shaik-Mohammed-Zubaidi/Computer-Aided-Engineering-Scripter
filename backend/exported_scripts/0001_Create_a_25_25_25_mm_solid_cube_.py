# Auto-exported from history.json
# User input: Create a 25 × 25 × 25 mm solid cube named Cube1

from abaqus import *
from abaqusConstants import *

# Create a new model database
Mdb()

# Create a new part named 'Cube1'
partName = 'Cube1'
cubeSize = 25.0  # Size of the cube in mm

# Create a solid cube
s = mdb.models['Model-1'].Part(name=partName, dimensionality=THREE_D, type=DEFORMABLE_BODY)
s.BaseSolidCube(size=cubeSize)
