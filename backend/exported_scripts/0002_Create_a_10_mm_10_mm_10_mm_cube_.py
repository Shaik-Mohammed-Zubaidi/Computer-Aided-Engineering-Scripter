# Auto-exported from history.json
# User input: Create a 10 mm × 10 mm × 10 mm cube named Cube1 assign Steel (E=210 GPa, ν=0.3), mesh with 5 mm elements and generate a job called CubeJob

from abaqus import *
from abaqusConstants import *

# Create a new model database
Mdb()

# Create a new model
modelName = 'Model-1'
model = mdb.models[modelName]

# Create a cube part
partName = 'Cube1'
cube = model.Part(name=partName, dimensionality=THREE_D, type=DEFORMABLE_BODY)
cube.BaseSolidCube(size=10.0)  # Create a 10 mm cube

# Define material properties for Steel
materialName = 'Steel'
steelMaterial = model.Material(name=materialName)
steelMaterial.Elastic(table=((210E9, 0.3),))  # E=210 GPa, ν=0.3

# Create a section and assign it to the cube
sectionName = 'SteelSection'
section = model.HomogeneousSolidSection(name=sectionName, material=materialName)
region = (cube.cells,)
cube.SectionAssignment(region=region, sectionName=sectionName)

# Mesh the part with 5 mm elements
cube.setMeshControls(elemShape=HEX, regions=cube.cells)
cube.generateMesh()

# Create a job for the model
jobName = 'CubeJob'
job = mdb.Job(name=jobName, model=modelName)

# Save the model database
mdb.save()
