

# archive class
class Archive:

	# constructor
	def __init__(self, archive_url, frequency, entry_number):
		self.archive_id = generate_archive_id()
		self.archive_url = archive_url
		self.frequency = frequency
		self.entry_number = get_entry_number(archive_url)

	# creates new archive in database
	def create_new_archive(archive_url, frequency, entry_number):

		# generate archive id

		# save new archive to user id
	
		# return archive id

		return None

	# checks number of entries pulled from current url, 
	# updates entry number if greater than saved number
	# TODO - needs internal timer to check automated searches monthly, weekly, etc.
	def check_entry_number(archive_url, entry_number, frequency):

		# check entry number pulled from current url

		# if new number > old number
			# get archive id
			# update entry number
			# get user id attached
			# send notification to user id - user class

		# returns nothing?

		return None

	# generates new archive id from database
	# should this be numbered based on user id or archive database?
	def generate_archive_id():

		# check archive ids in database

		# return last archive id + 1

		return None

	# saves new archive id under user's profile
	def save_new_archive(user_id, archive_id):
		# find user id

		# get archive array

		# append archive id to array

		# returns nothing or success?

		return None

	# updates entry number
	def update_entry_number(archive_id, new_entry_number):
		
		# finds archive id

		# sets entry number top new number

		# returns nothing or success?

		return None

	# update frequency of automated serach under user profile
	def update_frequency(archive_id, new_frequency):

		# finds archive id

		# sets frequency to new frequency

		# returns nothing or success?

		return None
