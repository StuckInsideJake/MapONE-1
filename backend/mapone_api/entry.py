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

	# creates new entry
	def create_new_entry(self, source_name, source_link, article_title,
		author_list, planet_flag, planet_name, region_name, map_scale):
		# generate entry id
		entry_id = self.generate_entry_id()

		# add to database
		Entry.objects.create(
			entry_id=entry_id,
			source_name=source_name,
			source_link=source_link,
			article_title=article_title,
			author_list=author_list,
			planet_flag=planet_flag,
			planet_name=planet_name,
			region_name=region_name,
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

	# TODO - filter functions, return list of entry ids

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
	def verify_entry(self, source_name, source_link, article_title, author_list,
		planet_flag, planet_name, region_name, map_scale):

		# check minimum requirements
		# only map scale can be None, unless non-planet? --> ask client

		# check planet flag? --> ask client
		
		# check existing
		entry_exists = self.check_existing_entry(article_title, author_list)

		# USGS database API check

		# if verified
		if(not entry_exists):
			# create new entry
			self.create_new_entry(
				source_name,
				source_link,
				article_title,
				author_list,
				planet_flag,
				planet_name,
				region_name,
				map_scale
			)

		# return success or fail
		return not entry_exists

	# stretch goal: clears database of invalid entries
	def clean_entries(self):
		# some criteria

		# get entry id

		# delete entry
		return None
