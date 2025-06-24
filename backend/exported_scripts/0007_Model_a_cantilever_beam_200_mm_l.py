# Auto-exported from history.json
# User input: Model a cantilever beam: 200 mm long, square cross-section 20 mm, mesh with B31 elements, fixed at X = 0, 1000 N tip load at X = 200, and output the tip displacement.

from abaqus import *
from abaqusConstants import *
import mesh

# Create a new model
model_name = 'CantileverBeam'
myModel = mdb.Model(name=model_name)

# Create a sketch for the beam profile
sketch = myModel.ConstrainedSketch(name='BeamProfile', sheetSize=100.0)
sketch.rectangle(point1=(0.0, 0.0), point2=(20.0, 20.0))  # 20 mm x 20 mm square cross-section

# Create a part from the sketch
beam_part = myModel.Part(name='CantileverBeam', dimensionality=THREE_D, type=DEFORMABLE_BODY)
beam_part.BaseSolidExtrude(sketch=sketch, depth=200.0)  # 200 mm length

# Create a material
material_name = 'Steel'
myMaterial = myModel.Material(name=material_name)
myMaterial.Elastic(table=((210E3, 0.3), ))  # Young's modulus in MPa and Poisson's ratio

# Create a section and assign it to the part
section_name = 'BeamSection'
mySection = myModel.HomogeneousSolidSection(name=section_name, material=material_name)
region = beam_part.Set(cells=beam_part.cells, name='BeamRegion')
beam_part.SectionAssignment(region=region, sectionName=section_name)

# Create an assembly
assembly = myModel.rootAssembly
instance = assembly.Instance(name='BeamInstance', part=beam_part, dependent=ON)

# Define the step for loading
myModel.StaticStep(name='LoadStep', previous='Initial')

# Apply boundary condition (fixed at X=0)
fixed_region = assembly.Set(vertices=instance.vertices.findAt(((0.0, 0.0, 0.0),)), name='FixedEnd')
myModel.EncastreBC(name='FixedBC', createStepName='LoadStep', region=fixed_region)

# Apply the tip load (1000 N at X=200)
load_region = assembly.Set(vertices=instance.vertices.findAt(((200.0, 10.0, 0.0),)), name='TipLoad')
myModel.ConcentratedForce(name='TipLoad', createStepName='LoadStep', region=load_region, cf1=-1000.0)  # Negative for downward load

# Mesh the part with B31 elements
beam_part.setMeshControls(elemShape=QUAD, regions=region, technique=STRUCTURED)
beam_part.generateMesh()

# Create a job and submit it
job_name = 'CantileverBeamJob'
myJob = mdb.Job(name=job_name, model=model_name, description='Job for cantilever beam analysis')
myJob.submit()
myJob.waitForCompletion()

# Output the tip displacement
odb_path = job_name + '.odb'
odb = session.openOdb(name=odb_path)
last_frame = odb.steps['LoadStep'].frames[-1]
displacement_field = last_frame.fieldOutputs['U']
tip_displacement = displacement_field.getSubset(region=load_region).values[0].data

# Print the tip displacement
print('Tip Displacement (mm):', tip_displacement[1] * 1000)  # Convert from m to mm
