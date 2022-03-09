from mapone_api.models import Entry
from django.db.models import Max, F, Q, CharField

# entry class
class EntryClass:

	# check if entry already exists
	def check_existing_entry(self, article_title, author_list):
		# TODO - may need reworking, similar values
		# look up article title and author list
		entry_exists = Entry.objects.filter(article_title=article_title, 
			author_list=author_list)

		# return if entry exists
		return len(list(entry_exists)) != 0

	# convert all datetime objects to strings
	def convert_date_to_string(self, entries):
		return None

	# creates new entry
	def create_new_entry(self, source_name, source_link, article_title,
		publication_date, author_list, map_body, map_scale):

		# generate entry id
		entry_id = self.generate_entry_id()

		# add to database
		Entry.objects.create(
			entry_id=entry_id,
			source_name=source_name,
			source_link=source_link,
			article_title=article_title,
			publication_date=publication_date,
			author_list=author_list,
			map_body=map_body,
			map_scale=map_scale
		)

		# return entry id
		return entry_id

	# remove entry
	def delete_entry(self, entry_id):
		# look up and delete entry
		Entry.objects.get(entry_id=entry_id).delete()

		# update user ids in database
		Entry.objects.filter(entry_id__gt=entry_id).update(
			entry_id=F('entry_id') - 1)

	# filter range for publication date
	def filter_year(self, first_year, second_year):
		# format date
		start_of_year = '-01-01'
		first_year += start_of_year
		second_year += start_of_year

		# get entries within year range
		year_match = Entry.objects.filter(publication_date__range=[first_year, second_year]).values()

		# if found results
		if year_match:
			# return list of entries
			return list(year_match)

		# return no results
		return None

	# generates entry id from database
	def generate_entry_id(self):
		# get largest entry id in database
		entry_id = Entry.objects.all().aggregate(Max('entry_id'))
		entry_id = entry_id['entry_id__max']

		# if no entry ids
		if(not entry_id):
			# return first entry value
			first_entry = 1
			return first_entry

		# return last entry id + 1
		return entry_id + 1

	# return all entries, call get data?
	def get_all_entries(self):
		# return all entries in database
		all_entries = Entry.objects.all().order_by('article_title').values()
		return list(all_entries)

	# return data array for each entry id pulled, append to a list
	# searches all text fields for keyword
	def search_keyword(self, keyword):
		# get all char fields
		fields = [field for field in Entry._meta.fields if isinstance(field, CharField)]
		
		# search keyword in fields
		queries = [Q(**{field.name: keyword}) for field in fields]
		
		# get results
		queryset = Q()
		for query in queries:
		    queryset = queryset | query

		keyword_match = Entry.objects.filter(queryset).order_by('article_title').values()

		# if keyword match
		if keyword_match:
			# return entries
			return list(keyword_match)

		# else return no results
		return None

	# verifies new entry collected by web scraper
	def verify_entry(self, source_name, source_link, article_title,
		publication_date, author_list, map_body, map_scale):
		# check existing
		entry_exists = self.check_existing_entry(article_title, author_list)

		# if verified
		if(not entry_exists):
			# reformat date
			year_length = 4
			year_month_length = 7

			if len(publication_date) == year_length:
				# add month and day
				publication_date += '-01-01'
			if len(publication_date) == year_month_length:
				# add day
				publication_date += '-01'

			# create new entry
			self.create_new_entry(
				source_name,
				source_link,
				article_title,
				publication_date,
				author_list,
				map_body,
				map_scale
			)

		# return success or fail
		return not entry_exists
