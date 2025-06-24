# Auto-exported from history.json
# User input: Add a material Steel (E = 210 GPa, ν = 0.3) and assign it to Cube1.

from abaqus import *
from abaqusConstants import *

# Create a new model database
mdb = Mdb()

# Create a new material named 'Steel'
steel_material = mdb.Material(name='Steel')
steel_material.Elastic(table=((210E9, 0.3),))  # E = 210 GPa, ν = 0.3

# Create a new part named 'Cube1'
cube1 = mdb.models['Model-1'].Part(name='Cube1', dimensionality=THREE_D, type=DEFORMABLE_BODY)

# Define the cube's geometry (1x1x1 unit cube)
cube1.BaseSolidCube(size=1.0)

# Create a section and assign the material to it
section = mdb.models['Model-1'].HomogeneousSolidSection(name='SteelSection', material='Steel')
cube1.SectionAssignment(region=cube1.Set(cells=cube1.cells, name='Cube1Set'), sectionName='SteelSection')
