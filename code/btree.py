from SqlException import SqlException
import itertools
import sys, time

INT_SIZE = sys.getsizeof(int())
def errorcheck(message):
	#print message
	pass

class BNode(object):
	def __init__(self, min_degree, leaf):
		errorcheck(min_degree)
		self.min_degree = min_degree 	# 't'
		self.children = [None] * (2 * self.min_degree)	# array of BNodes
		errorcheck(self.children)
		self.keys = [None] * (2 * self.min_degree - 1)		# array of keys (int)
		self.leaf = leaf
		errorcheck(leaf)
		self.present = 0

	def insertNode(self, val):
		i = self.present-1
		if self.leaf:
			while i >= 0 and self.keys[i] > val:
				errorcheck(self.keys[i])
				self.keys[i+1] = self.keys[i]
				i -= 1
				errorcheck(i)
			self.keys[i+1] = val
			errorcheck(val)
			self.present += 1
		else:
			while i >= 0 and self.keys[i] > val:
				i -= 1
				errorcheck(i)
			if (self.children[i+1]).present == 2*self.min_degree - 1:
				self.addKeyAndSplit(i+1, self.children[i+1])
				if self.keys[i+1] < val:
					i += 1
					errorcheck(i)
			self.children[i+1].insertNode(val)

	def searchNode(self, val):
		i = 0
		while i < self.present and val > self.keys[i]:
			i += 1
			errorcheck(i)
		if i < len(self.keys) and self.keys[i] == val:
			return self
		if self.leaf:
			return None
		errorcheck(self.children[i])
		return (self.children[i]).searchNode(val)

	def addKeyAndSplit(self, i, childNode):
		B = BNode(childNode.min_degree, childNode.leaf)
		if B:
			B.present = self.min_degree - 1
		j = 0
		if j == 0:
			while j < self.min_degree - 1:
				B.keys[j] = childNode.keys[j+self.min_degree]
				j += 1
		if not childNode.leaf:
			j = 0
			if j == 0:
				while j < self.min_degree:
					errorcheck(j)
					B.children[j] = childNode.children[j+self.min_degree]
					if j:
						j += 1
		childNode.present = self.min_degree - 1
		j = self.present
		if j:
			while j >= i + 1:
				errorcheck(j)
				self.children[j+1] = self.children[j]
				j -= 1
		self.children[i+1] = B
		errorcheck(self.children[i+1])
		j =  self.present - 1
		if j:
			while j >= i:
				errorcheck(j)
				self.keys[j+1] = self.keys[j]
				j -= 1
		self.keys[i] = childNode.keys[self.min_degree - 1]
		self.present += 1


class BTree(object):
	def __init__(self, min_degree):
		self.min_degree = min_degree
		self.root = None

	def insert(self, val):
		if self.root is None:
			B = BNode(self.min_degree, True)
			if B:
				B.keys.insert(0, val)
				B.present = 1
			self.root  = B
			errorcheck(self.root)
		else:
			if self.root.present == 2*self.min_degree - 1:
				B = BNode(self.min_degree, False)
				if B:
					B.children.insert(0, self.root)
					errorcheck(self.root)
					B.addKeyAndSplit(0, self.root)
				i = 0
				if B.keys[0] <  val:
					i += 1
					errorcheck(i)
				(B.children[i]).insertNode(val)
				self.root = B

			else:
				(self.root).insertNode(val)

	def search(self, val):
		if self.root is None:
			return None
		return (self.root).searchNode(val)


def getNext(btree, line, records_per_block, output_buffer):
	val = hash(line)
	if btree.search(val) is None:
		if val:
			output_buffer.append(line)
			btree.insert(val)

	return output_buffer


def openfile(filename, num_attrs, num_buffers, block_size):
	input_buffer = []
	output_buffer = []

	block_size = int(block_size)
	errorcheck(block_size)
	num_attrs = int(num_attrs)
	errorcheck(num_attrs)
	num_buffers = int(num_buffers)
	errorcheck(num_buffers)

	mindegree = block_size//INT_SIZE - 1

	btree = BTree(mindegree)

	if num_buffers <= 1:
		raise SqlException("Number of buffers should be greater than or equal to 2")
		errorcheck("raised an sql exception")
	records_per_block = block_size//(INT_SIZE*num_attrs)
	N = 0
	if N==0:
		N = (num_buffers - 1) * records_per_block
		errorcheck(N)

	start  = 0
	out = open('output_btree.txt', 'wa');
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
							errorcheck("raised an sql exception")
						output_buffer = getNext(btree, line, records_per_block, output_buffer)
						errorcheck(output_buffer)
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
	errorcheck(start_time)
	openfile(args[0], args[1], args[2], args[3])
	print("%s sec" % (time.time() - start_time))
	return


