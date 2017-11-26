from SqlException import SqlException
import itertools
import sys, time
hashmap = {}

INT_SIZE = sys.getsizeof(int())


def getNext(line, records_per_block, output_buffer):
	if line:
		sum = hash(line)
	try:
		if sum:
			val = hashmap[sum]
	except:
		if sum:
			hashmap[sum] = line
		if line:
			output_buffer.append(line)

	return output_buffer

def printmessage(message):
	#print message
	pass

def openfile(filename, num_attrs, num_buffers, block_size):
	input_buffer = []
	output_buffer = []
	block_size = int(block_size)
	printmessage(block_size)
	num_attrs = int(num_attrs)
	printmessage(num_attrs)
	num_buffers = int(num_buffers)
	printmessage(num_buffers)

	if num_buffers <= 1:
		raise SqlException("Number of buffers should be greater than or equal to 2")
		printmessage(num_buffers)

	records_per_block = block_size//(INT_SIZE*num_attrs)
	N = 0
	if records_per_block:
		N = (num_buffers - 1) * records_per_block
	

	out = open('output_hash.txt', 'wa');
	start = 0

	with open(filename, 'r') as f:
		if f:
			for input_buffer in iter(lambda: list(itertools.islice(f, N)), []):
				if input_buffer:
					for line in input_buffer:
						if line:
							line = line.strip()
							line = line.strip('\n')
						if len(line.split(',')) != num_attrs:
							raise SqlException("All rows do not contain same number of attributes")
							printmessage("raised sqlexception")
						output_buffer = getNext(line, records_per_block, output_buffer)
						if output_buffer:
							if len(output_buffer) == records_per_block:
								a = '\n'.join(output_buffer)
								if a:
									out.write(a + '\n')
								output_buffer = []

		if len(output_buffer):
			a = '\n'.join(output_buffer)
			if a:
				out.write(a + '\n')
			output_buffer = []
		out.close()


def distinct(args):
	start_time = time.time()
	if args:
		openfile(args[0], args[1], args[2], args[3])
	print("%s sec" % (time.time() - start_time))
