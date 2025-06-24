# Auto-exported from history.json
# User input: Create a job called CubeJob, run it, and wait for completion.

from abaqus import *
from abaqusConstants import *

# Create a job named 'CubeJob'
job = mdb.Job(name='CubeJob', model='Model-1')

# Submit the job for execution
job.submit()

# Wait for the job to complete
job.waitForCompletion()
