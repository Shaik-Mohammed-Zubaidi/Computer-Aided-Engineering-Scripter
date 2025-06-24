# Auto-exported from history.json
# User input: Mesh the cube with 5 mm elements and print the total element count

from abaqus import *
from abaqusConstants import *
import mesh

# Create a new model database
Mdb()

# Create a cube part
partName = 'Cube'
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=10.0)
s.rectangle(point1=(-5.0, -5.0), point2=(5.0, 5.0))
p = mdb.models['Model-1'].Part(name=partName, dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=10.0)

# Define the mesh size
elementSize = 5.0

# Generate the mesh
p.setMeshControls(elemShape=HEX, regions=(p.cells,), technique=STRUCTURED)
p.seedPart(size=elementSize, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()

# Get the total element count
totalElements = len(p.elements)

# Print the total element count
print('Total element count:', totalElements)
