from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

### INPUT DATA HERE ###
if rank == 0:
    data = [1,2,3,4,5,6,8,242]
else:
    data = []

# Distribute
if rank == 0:
	comm_s = comm.Get_size()
	data_s = len(data)

	
	if data_s < comm_s:
		# data size < comm size, pad with Nones
		while data_s < comm_s:
			data.append(None)
			data_s = len(data)
	elif data_s > comm_s:
		# data size > comm size, pad with Nones
		# till data size is a multiple of comm size
		while (data_s % comm_s) != 0:
			data.append(None)
			data_s = len(data)
		# data_s is now a multiple of comm_s
		fraction = (data_s / comm_s)
		new_data = []
		group_list = []
		index = 0
		for d in data:
			index += 1
			group_list.append(d)
			if (index % fraction) == 0:
				new_data.append(group_list)
				group_list = []
		data = new_data

data = comm.scatter(data, root=0)

# Filter
if type(data) != list:
	if data == None:
		pass
		# only have this clause
		# to avoid modding None type
	elif (data % 2) != 0:
		data = None
elif type(data) == list:
	filtered_data = []
	for d in data:
		if d == None:
			filtered_data.append(d)
		elif (d % 2) == 0:
			filtered_data.append(d)
		else:
			filtered_data.append(None)
	data = filtered_data


# Gather
data = comm.gather(data, root=0)
comm.Barrier()

if rank == 0:
	# concatenate data if data is a list of lists:
	concat_data = []
	for d in data:
		if type(d) != list:
			break
			# no need to concatenate
		else:
			concat_data.extend(d)

	if concat_data:
		data = concat_data

	final_data = []
	# remove all None's from data
	for d in data:
		if d != None:
			final_data.append(d)
	data = final_data

	print data 

