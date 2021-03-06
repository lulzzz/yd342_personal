import math
import numpy as np
from mpi4py import MPI
from LakeModel_IT import LakeModel_IT

# Read in Latin hypercube samples of uncertain parameters
LHsamples = np.loadtxt('./../LHsamples.txt')

# Read in result file from intertemporal optimization
IT = np.loadtxt('./../../Optimization/Intertemporal.resultfile')

# Define the number of objectives and constraints
nobjs = 4

# Begin parallel simulation
comm = MPI.COMM_WORLD

# Get the number of processors and the rank of processors
rank = comm.rank
nprocs = comm.size

# Determine the chunk which each processor will neeed to do
count = int(math.floor(np.shape(IT)[0]/nprocs))
remainder = np.shape(IT)[0] % nprocs

# Use the processor rank to determine the chunk of work each processor will do
if rank < remainder:
	start = rank*(count+1)
	stop = start + count + 1
else:
	start = remainder*(count+1) + (rank-remainder)*count
	stop = start + count

# Initialize matrices to store all objectives and constraints when evaluating these policies
# across all Latin hypercube samples of uncertain parameter values
ITobjs = np.zeros([stop-start,np.shape(LHsamples)[0],nobjs])

# Run simulation
for i in range(start, stop):
	row = i-start
	for j in range(np.shape(LHsamples)[0]):
		ITobjs[row,j,:]= LakeModel_IT(1, IT[i,0:100], LHsamples[j,0], LHsamples[j,1], \
		LHsamples[j,2], LHsamples[j,3], LHsamples[j,4], LHsamples[j,5])

	# Write output to file labeled by Pareto point index
	filename = "./output/ITobjs_%i.txt" % i
	np.savetxt(filename, ITobjs[row,:,:])
