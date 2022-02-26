from datetime import date
import calendar
import schedule

from mapone_api.models import Archive, User

from mapone_api.user import UserClass
from mapone_api.entry import EntryClass

from django.db.models import Max, F


# archive class
class ArchiveClass:

	# creates new archive in database
	def create_new_archive(self, user_id, keyword, frequency):
		# get user object
		user_class = UserClass()
		user_object = User.objects.get(user_id=user_id)

		# generate archive id
		archive_id = self.generate_archive_id()

		# get entry number
		entry_number = self.get_entry_number(keyword)

		# add to database
		Archive.objects.create(
			user_id=user_object,
			archive_id=archive_id,
			keyword=keyword,
			frequency=frequency,
			entry_number=entry_number
		)

		# return archive id
		return archive_id

	# checks number of entries pulled from current keyword search 
	# updates entry number if greater than saved number
	def check_entry_number(self, archive_id, keyword, past_entry_number):
		# check current entry number from keyword search
		current_entry_number = self.get_entry_number(keyword)

		# if new number > old number
		if current_entry_number > past_entry_number:
			# get archive id
			saved_archive = Archive.objects.filter(archive_id=archive_id).values()

			# update entry number
			saved_archive.update(entry_number=current_entry_number)

			# get user id attached
			user_id = list(saved_archive)[0]['user_id_id']

			# send notification to user id
			# call user class
			user_class = UserClass()
			subject = 'MapONE: Automated Search Update'
			message = f'There are new map additions to your {keyword} automated search.'
			message += 'Visit USGS.gov/MapONE to view your results.'
			user_class.send_notification(user_id, subject, message)

	# remove automated search
	def delete_archive(self, archive_id):
		# look up and delete automated search
		Archive.objects.get(archive_id=archive_id).delete()

		# update archive ids in database
		Archive.objects.filter(archive_id__gt=archive_id).update(
			archive_id=F('archive_id') - 1)

	# generates new archive id from database
	def generate_archive_id(self):
		# get largest archive id in database
		archive_id = Archive.objects.all().aggregate(Max('archive_id'))
		archive_id = archive_id['archive_id__max']

		# if no archive ids
		if(not archive_id):
			# return first entry value
			first_entry = 1
			return first_entry

		# return last archive id + 1
		return archive_id + 1

	# gets entry number from results pulled from search keyword
	def get_entry_number(self, keyword):
		# get results from keyword search
		# call the entry class
		entry_class = EntryClass()
		results = entry_class.search_keyword(keyword)

		# if not null
		if results:
			# return number of entries
			return len(results)

		# else, return 0 results
		return 0

	# pulls all archive ids with a given frequency
	def get_searches_by_frequency(self, frequency):
		# set id list
		id_list = []

		# get all searches with given frequency
		archive_ids = Archive.objects.filter(frequency=frequency).values('archive_id')

		# loop across archive ids
		for archive_id in archive_ids:
			id_list.append(archive_id['archive_id'])
		
		# return list
		return id_list

	# get all archive data under a user id
	def get_user_saved_searches(self, user_id):
		# get all saved searches under a user id
		saved_searches = Archive.objects.filter(user_id=user_id).values()

		# return list of search info
		return list(saved_searches)

	# checks automated searches by frequency
	def run_frequency(self, frequency):
		# get search results
		results = self.get_searches_by_frequency(frequency)

		# if not null
		if results:
			for archive_id in results:
				# look up archive object
				archive = Archive.objects.filter(archive_id=archive_id).values()
				archive = list(archive)[0]
				
				# check entry number
				self.check_entry_number(
					archive_id,
					archive['keyword'],
					archive['entry_number']
				)

	# sets internal timer to run automated searches
	# RUN THIS FUNCTION EVERY DAY --> TODO: where to call?
	def run_schedule(self):
		# get daily data
		today = date.today()
		day = today.day
		day_of_week = calendar.day_name[today.weekday()]
		first_of_week = 'Monday'
		first_of_month = 1
		halfway_month = 15

		# run daily searches
		self.run_frequency('daily')

		if day == first_of_month:
			# run monthly & biweekly searches
			self.run_frequency('month')
			self.run_frequency('biweek')

		if day == halfway_month:
			# run biweekly searches
			self.run_frequency('biweek')

		if day == first_of_week:
			# run weekly searches
			self.run_frequency('week')		

	# update frequency of automated search
	def update_frequency(self, archive_id, new_frequency):
		# find archive id, update frequency
		Archive.objects.filter(archive_id=archive_id).update(
			frequency=new_frequency)
