# Auto-exported from history.json
# User input: Build two concentric cylinders (r = 40 mm and 50 mm) and subtract to make a hollow pipe 400 mm long; mesh, assign aluminum, and evaluate hoop stress at mid-length

from abaqus import *
from abaqusConstants import *

# Create a new model
modelName = 'HollowPipeModel'
myModel = mdb.Model(name=modelName)

# Create a sketch for the outer cylinder
s = myModel.ConstrainedSketch(name='OuterCylinderSketch', sheetSize=100.0)
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(50.0, 0.0))  # Outer radius 50 mm

# Create the outer cylinder part
outerCylinder = myModel.Part(name='OuterCylinder', dimensionality=THREE_D, type=DEFORMABLE_BODY)
outerCylinder.BaseSolidExtrude(sketch=s, depth=400.0)  # Length 400 mm

# Create a sketch for the inner cylinder
s = myModel.ConstrainedSketch(name='InnerCylinderSketch', sheetSize=100.0)
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(40.0, 0.0))  # Inner radius 40 mm

# Create the inner cylinder part
innerCylinder = myModel.Part(name='InnerCylinder', dimensionality=THREE_D, type=DEFORMABLE_BODY)
innerCylinder.BaseSolidExtrude(sketch=s, depth=400.0)  # Length 400 mm

# Create a boolean operation to subtract the inner cylinder from the outer cylinder
hollowPipe = myModel.Part(name='HollowPipe', dimensionality=THREE_D, type=DEFORMABLE_BODY)
hollowPipe = outerCylinder.copy()  # Copy outer cylinder
hollowPipe.Set(name='OuterSet', cells=hollowPipe.cells)  # Set for outer cylinder
myModel.parts['HollowPipe'].Boolean(name='SubtractInner', operation=SUBTRACT, 
                                     toolParts=(innerCylinder,))

# Assign material properties
materialName = 'Aluminum'
myMaterial = myModel.Material(name=materialName)
myMaterial.Elastic(table=((70000.0, 0.33),))  # Young's modulus and Poisson's ratio for aluminum

# Create a section and assign it to the hollow pipe
sectionName = 'PipeSection'
mySection = myModel.HomogeneousSolidSection(name=sectionName, material=materialName)
hollowPipe.SectionAssignment(region=hollowPipe.Set(name='HollowPipeSet', cells=hollowPipe.cells), sectionName=sectionName)

# Mesh the hollow pipe
hollowPipe.seedPart(size=10.0)  # Seed size for mesh
hollowPipe.generateMesh()  # Generate the mesh

# Create a job and submit it for analysis
jobName = 'HollowPipeJob'
myJob = mdb.Job(name=jobName, model=modelName, description='Job for hollow pipe analysis')
myJob.submit()
myJob.waitForCompletion()

# Evaluate hoop stress at mid-length
from odbAccess import *
odb = openOdb(path=jobName+'.odb')
step = odb.steps[odb.steps.keys()[-1]]  # Get the last step
frame = step.frames[-1]  # Get the last frame
stressField = frame.fieldOutputs['S']  # Get stress field output
hoopStress = stressField.getSubset(region=hollowPipe.Set(name='HollowPipeSet', cells=hollowPipe.cells)).values

# Extract and print hoop stress values
for stress in hoopStress:
    if stress.label == 'S22':  # Hoop stress component
        print('Hoop Stress at mid-length:', stress.data)  # Print hoop stress value

odb.close()  # Close the ODB file
