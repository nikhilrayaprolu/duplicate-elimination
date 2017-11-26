class SqlException(Exception):
	def __init__(self, arg):
		self.message = arg
