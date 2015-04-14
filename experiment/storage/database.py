
class DictDatabase(object):
	def __init__(self):
		self.content = {}
		self.next_id = 0
	
	def store(self, item):
		next_id = self.next_id
		self.next_id+=1
		self.content[next_id] =  item
		return next_id

	def get(self, item_id):
		return self.content[item_id]

	def get_all_ids(self, ):
		return self.content.keys()

	def delete(self, item_id):
		del self.content[item_id]

drafts = DictDatabase()
experiments = DictDatabase()