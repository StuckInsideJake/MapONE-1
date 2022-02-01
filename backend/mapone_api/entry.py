

# entry class
class Entry:

	# constructor
	def __init__(self, source_name, source_link, map_area,
		map_scale, author_name):
		self.entry_id = generate_entry_id()
		self.source_name = source_name
		self.source_link = source_link
		self.map_area = map_area
		self.map_scale = map_scale
		self.author_name = author_name

	# creates new entry
	def create_new_entry(source_name, source_link, map_area, 
		map_scale, author_name):
		# verify entry

		# if verified
			# generate entry id

		# add to database

		# return entry id

		return None

	# generates entry id from database
	def generate_entry_id():
		# check entry ids in database

		# return last entry id + 1

		return None

	# searches map area filter, returns all entry ids with filter
	def search_map_area(map_area):
		# checks through all entries
			# if map area
				# add entry id to list

		# returns list of entry ids

		return None

	# searches source name filter, returns all entry ids with filter
	def search_source_name(source_name):
		# checks through all entries
			# if source name
				# add entry id to list

		# returns list of entry ids

		return None

	# verifies new entry collected by web scraper
	def verify_entry(source_name, source_link, map_area, 
		map_scale, author_name):
		# API check

		# other constraints

		# if verified
			# create new entry

		# return success or fail

		return None

	# need to add clean process to delete bad entries
	# and update entry ids
