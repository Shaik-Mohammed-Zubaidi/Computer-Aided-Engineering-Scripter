# Auto-exported from history.json
# User input: Parameterize the cube edge length as variable L = 10, 20, 30 mm and run three analyses in a loop

from abaqus import *
from abaqusConstants import *
import job

# Define the edge lengths for the cube
edge_lengths = [10.0, 20.0, 30.0]  # in mm

# Loop through each edge length
for L in edge_lengths:
    # Create a new model
    model_name = f'CubeModel_L{L}'
    mdb.Model(name=model_name)
    
    # Create a sketch for the cube
    s = mdb.models[model_name].ConstrainedSketch(name='CubeSketch', sheetSize=2*L)
    s.rectangle(point1=(0, 0), point2=(L, L))  # Create a square base
    
    # Create a part from the sketch
    p = mdb.models[model_name].Part(name='Cube', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p.BaseSolidExtrude(sketch=s, depth=L)  # Extrude to form a cube
    
    # Create a material
    material_name = 'Steel'
    mdb.models[model_name].Material(name=material_name)
    mdb.models[model_name].materials[material_name].Elastic(table=((210E3, 0.3),))  # Young's modulus and Poisson's ratio
    
    # Create a section and assign it to the cube
    section_name = 'CubeSection'
    mdb.models[model_name].HomogeneousSolidSection(name=section_name, material=material_name)
    region = p.Set(cells=p.cells, name='CubeRegion')
    p.SectionAssignment(region=region, sectionName=section_name)
    
    # Create an assembly
    a = mdb.models[model_name].rootAssembly
    a.Instance(name='CubeInstance', part=p, dependent=ON)
    
    # Create a step for analysis
    mdb.models[model_name].StaticStep(name='LoadStep', previous='Initial')
    
    # Create a job and submit it
    job_name = f'CubeJob_L{L}'
    mdb.Job(name=job_name, model=model_name, description='Job for cube analysis', type=ANALYSIS)
    mdb.jobs[job_name].submit()
    mdb.jobs[job_name].waitForCompletion()  # Wait for the job to complete before proceeding
