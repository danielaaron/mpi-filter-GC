from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    data = [1,2,3,4,5]
else:
    data = []

#Scatter
data = comm.scatter(data, root=0)
print "rank", rank, "recieved", data

#Filter
new_data = []
for d in data:
	if d % 2 == 0:
		new_data.append(d)
data = new_data


#Gather
data = comm.gather(data, root=0)

comm.Barrier()

if rank == 0:
    print data