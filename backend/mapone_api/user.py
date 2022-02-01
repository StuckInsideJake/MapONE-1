

# user class
class User:

	# constructor
	def __init__(self, email_address, password):
		self.user_id = generate_user_id()
		self.email_address = email_address
		self.password = password
		self.archive_id_array = ''

	# creates new user, returns user id
	def create_new_user(email_address, password):
		# verify email address (flag)

		# verify password (flag)

		# if both verified
			# generate user id

		# add to database
		
		# return user id
		return None

	# creates new user id, returns user id
	def generate_user_id():
		# check user ids in database

		# return last user id + 1

		return None

	# sends email to inform user on automated search updates
	def send_notification(user_id, message):
		# gets user's email address

		# sends email to message

		# return success or fail

		return None

	# verifies new email address
	def verify_email_address(email_address):
		# check if email address is not under another user

		# validates email address using API or built-in Django
		# feature

		# returns success or fail

		return None

	# verifies new password
	def verify_password(password):
		# checks if password meets all requirements
		# length, special chars, etc.

		# returns success or fail

		return None

	# checks if user is valid
	def verify_user(email_address, password):
		# checks database for email address

		# checks if password matches email address
		# under same user id

		# return if both verified (success or fail)

		return None

