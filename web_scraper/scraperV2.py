# Importing urllib.request to use urlopen
from urllib.request import build_opener, HTTPCookieProcessor
# Importing urllib.error to handle errors in HTTP pinging
import urllib.error
# BeautifulSoup is used for scraping
from bs4 import BeautifulSoup as bs
# Counter generates a dictionary from the abstract data, providing frequencies of occurences
from collections import Counter
# Importing the CSV library here to dump the dictionary for further analysis and error checking if required. Will edit it out later
import csv
# Importing numpy to generate a random integer for the delay_function (see below)
import numpy as np
# This library is imported to check if we can feasibly introduce delays into the processor loop to reduce instances of the remote server, 
# shutting the connection while scrapping extraordinarily large datasets
import time
# Fragmenting code into different scripts. Some functions are to be used across the different sub-parts as well. 
# Hence, shifted some of the functions to the new script
from common_functions import pre_processing, argument_formatter, keyword_url_generator, abstract_id_log_name_generator, status_logger

def url_reader(url, status_logger_name):
	# This keyword is supplied to the URL and is hence used for souping.
	# Encountered an error where some links would not open due to HTTP.error
	# Attempts to ping the page, and if not, move on to the next
	try:
		# Using the urllib function w/ urlopen to extract the html_code of the given page
		open_connection = build_opener(HTTPCookieProcessor())
		html_code = open_connection.open(url)
		# Close the abstract window after each abstract has been extracted
		return html_code			
	except (UnboundLocalError, urllib.error.HTTPError):
		pass

def results_determiner(url, status_logger_name):
	# Determines the number of results a particular keyword returns
	first_page_to_scrape = url_reader(url, status_logger_name)

	first_page_to_scrape_soup = page_souper(first_page_to_scrape, status_logger_name)
	number_of_results = first_page_to_scrape_soup.find('h1', {'id':'number-of-search-results-and-search-terms'}).find('strong').text

	results_determiner_status_key = "Total number of results obtained: "+number_of_results
	status_logger(status_logger_name, results_determiner_status_key)

def url_generator(start_url, query_string, status_logger_name):
	# This function scrapes all possible webpages of a given topic
	# The search for the URLs truncates when determiner variable doesn't return a positive value
	url_generator_start_status_key = start_url + " start_url has been received"
	status_logger(status_logger_name, url_generator_start_status_key)

	# Initiallizing a list in order to contain the URLs
	urls_to_scrape = []
	counter = 0
	total_url = start_url + str(counter) +  "?facet-content-type=\"Article\"&query=" + query_string + "&facet-language=\"En\""
	initial_url_status_key = total_url + " has been obtained"

	status_logger(status_logger_name, initial_url_status_key)
    
	urls_to_scrape.append(total_url)
	test_soup = bs(url_reader(total_url, status_logger_name), 'html.parser')

	# Grabs the page element that contains the number of pages to be scrapped
	determiner = test_soup.findAll('span', {'class':'number-of-pages'})[0].text

	# Generate the urls_to_scrape from the stripped down determiner element
	urls_to_scrape = [(start_url + str(counter) + "?facet-content-type=\"Article\"&query=" + 
    query_string + "&facet-language=\"En\"") for counter in range(1, (int(determiner.replace(',', '')) + 1))]
	
	url_generator_stop_status_key = determiner.replace(',', '') + " page URLs have been obtained"
	status_logger(status_logger_name, url_generator_stop_status_key)

	return urls_to_scrape

def page_souper(page, status_logger_name):
	# Soups the web page elements and provides tags for scraping
	page_souper_start_status_key = "Souping page"
	status_logger(status_logger_name, page_souper_start_status_key)

	page_soup = bs(page, 'html.parser')

	page_souper_stop_status_key = "Souped page"
	status_logger(status_logger_name, page_souper_stop_status_key)

	return page_soup

def abstract_word_extractor(abstract, abstract_title, abstract_year, permanent_word_sorter_list, trend_keywords, status_logger_name):
	# Creates the list that stores the text in the form of individual words against their year of appearence
	abstract_word_sorter_start_status_key = "Adding: " + abstract_title + " to the archival list"
	status_logger(status_logger_name, abstract_word_sorter_start_status_key)
	
	# Converts the entire abstract into lower case
	abstract = abstract.lower()

	# Converts abstract into a list of words
	abstract_word_list = abstract.split()

	# Sorts the elements in the word list alphabetically
	abstract_word_list.sort()
	# If the word in the abstract list matches, the year it appears is appended to the permanent word sorter list
	for element in abstract_word_list:
		if(element==trend_keywords[0]):
			permanent_word_sorter_list.append(abstract_year[:4])

	abstract_word_sorter_end_status_key = "Added: " + abstract_title + " to the archival list"
	status_logger(status_logger_name, abstract_word_sorter_end_status_key)

def abstract_year_list_post_processor(permanent_word_sorter_list, status_logger_name):
	# Because of this function we have a dictionary containing the frequency of occurrence of terms in specific years
	abstract_year_list_post_processor_start_status_key = "Post processing of permanent word sorter list has commenced"
	status_logger(status_logger_name, abstract_year_list_post_processor_start_status_key)

	abstract_year_dictionary = Counter(permanent_word_sorter_list)

	abstract_year_list_post_processor_end_status_key = "Post processing of permanent word sorter list has completed"
	status_logger(status_logger_name, abstract_year_list_post_processor_end_status_key)

	return abstract_year_dictionary

def abstract_year_dictionary_dumper(abstract_word_dictionary, abstracts_log_name, status_logger_name):
	# Saves the abstract word dumper as a CSV
	permanent_word_sorter_list_start_status_key = "Dumping the entire dictionary to the disc"
	status_logger(status_logger_name, permanent_word_sorter_list_start_status_key)

	with open(abstracts_log_name+"_"+"DICTIONARY.csv", 'w') as dictionary_to_csv:
		writer = csv.writer(dictionary_to_csv)
		for key, value in abstract_word_dictionary.items():
			year = key
			writer.writerow([year, value])
	
	permanent_word_sorter_list_end_status_key = "Dumped the entire dictionary to the disc"
	status_logger(status_logger_name, permanent_word_sorter_list_end_status_key)

def abstract_page_scraper(abstract_url, abstract_input_tag_id, abstracts_log_name, permanent_word_sorter_list, site_url_index, status_logger_name):
	# Scrapes the actual abstract of the specific paper
	abstract_page_scraper_status_key = "Abstract ID: " + abstract_input_tag_id
	status_logger(status_logger_name, abstract_page_scraper_status_key)
	
	abstract_page_url = abstract_url+abstract_input_tag_id
	abstract_page = url_reader(abstract_page_url, status_logger_name)
	abstract_soup = page_souper(abstract_page, status_logger_name)
	title = title_scraper(abstract_soup, status_logger_name)
	abstract_date = abstract_date_scraper(title, abstract_soup, status_logger_name)

	# Failsafe for author attribute errors
	try:
		author = author_scraper(abstract_soup, status_logger_name)
	except AttributeError:
		author = "Author not available"

	# Failsafe for abstract scraping errors
	try:
		abstract = abstract_scraper(abstract_soup)
		# abstract_word_extractor(abstract, title, abstract_date, permanent_word_sorter_list, trend_keywords, status_logger_name)
	except AttributeError:
		abstract = "Abstract not available"

	abstract_database_writer(abstract_page_url, title, author, abstract, abstracts_log_name, abstract_date, status_logger_name)
	analytical_abstract_database_writer(title, author, abstract, abstracts_log_name, status_logger_name)

def abstract_scanner(abstract_url, abstract_id_log_name, abstracts_log_name, permanent_word_sorter_list, site_url_index, status_logger_name):
	abstract_crawler_start_status_key = "Entered the Abstract Scanner"
	status_logger(status_logger_name, abstract_crawler_start_status_key)
	
	abstract_crawler_temp_index  = site_url_index
	# This function crawls the page and access each and every abstract
	abstract_input_tag_ids = abstract_id_database_reader(abstract_id_log_name, abstract_crawler_temp_index, status_logger_name)
	for abstract_input_tag_id in abstract_input_tag_ids:
		try:
			abstract_scanner_accept = "Abstract Number: " + str((abstract_input_tag_ids.index(abstract_input_tag_id) 
            + 1) + abstract_crawler_temp_index * 20)

			status_logger(status_logger_name, abstract_scanner_accept)

			abstract_page_scraper(abstract_url, abstract_input_tag_id, abstracts_log_name, permanent_word_sorter_list, 
            site_url_index, status_logger_name)

		except TypeError:
			abstract_scanner_reject = "Abstract Number: " + str(abstract_input_tag_ids.index(abstract_input_tag_id) 
            + 1) + " could not be processed"

			status_logger(status_logger_name, abstract_scanner_reject)
			pass

	abstract_crawler_end_status_key = "Exiting the Abstract Scanner"
	status_logger(status_logger_name, abstract_crawler_end_status_key)

def analytical_abstract_database_writer(title, author, abstract, abstracts_log_name, status_logger_name):
	'''This function will generate a secondary abstract file that will contain only the abstract.
	The abstract file generated will be passed onto the Visualizer and Analyzer function, as opposed to the complete 
	abstract log file containing lot of garbage words in addition to the abstract text.'''
	analytical_abstract_database_writer_start_status_key = "Writing"+" "+title+" "+"by"+" "+author+" "+"to analytical abstracts file"
	status_logger(status_logger_name, analytical_abstract_database_writer_start_status_key)

	analytical_abstracts_txt_log = open(abstracts_log_name+'_'+'ANALYTICAL'+'.txt', 'a')
	analytical_abstracts_txt_log.write(abstract)
	analytical_abstracts_txt_log.write('\n'+'\n')
	analytical_abstracts_txt_log.close()

	analytical_abstract_database_writer_stop_status_key = "Written"+" "+title+" "+"to disc"
	status_logger(status_logger_name, analytical_abstract_database_writer_stop_status_key)

def abstract_database_writer(abstract_page_url, title, author, abstract, abstracts_log_name, abstract_date, status_logger_name):
	# Makes text/csv files to contain the abstracts for future reference
	# It holds: 1) Title, 2) Author(s), 3) Abstract
	abstract_database_writer_start_status_key = "Writing " + title + " by " + author + " to disc"
	status_logger(status_logger_name, abstract_database_writer_start_status_key)
	
	abstracts_csv_log = open(abstracts_log_name + '.csv', 'a')
	abstracts_txt_log = open(abstracts_log_name + '.txt', 'a')
	abstracts_txt_log.write("Title: " + title)
	abstracts_txt_log.write('\n')
	abstracts_txt_log.write("Author: " + author)
	abstracts_txt_log.write('\n')
	abstracts_txt_log.write("Date: " + abstract_date)
	abstracts_txt_log.write('\n')
	abstracts_txt_log.write("URL: " + abstract_page_url)
	abstracts_txt_log.write('\n')
	abstracts_txt_log.write("Scale: ")
	abstracts_txt_log.write('\n'+'\n')
	abstracts_txt_log.close()
	abstracts_csv_log.close()

	abstract_database_writer_stop_status_key = "Written " + title + " to disc"
	status_logger(status_logger_name, abstract_database_writer_stop_status_key)

def abstract_id_database_reader(abstract_id_log_name, site_url_index, status_logger_name):
	# Access to the database this program generates
	abstract_id_reader_temp_index = site_url_index
	abstract_id_database_reader_start_status_key = "Extracting Abstract IDs from disc"
	status_logger(status_logger_name, abstract_id_database_reader_start_status_key)

	lines_in_abstract_id_database=[line.rstrip('\n') for line in open(abstract_id_log_name + 
    str(abstract_id_reader_temp_index + 1) + '.txt')]

	abstract_id_database_reader_stop_status_key = "Extracted Abstract IDs from disc"
	status_logger(status_logger_name, abstract_id_database_reader_stop_status_key)

	return lines_in_abstract_id_database

def abstract_id_database_writer(abstract_id_log_name, abstract_input_tag_id, site_url_index):
	# Writes the abtract IDs to a .txt file for easy access and documentation
	abstract_id_writer_temp_index  = site_url_index
	abstract_id_log = open((abstract_id_log_name + str(abstract_id_writer_temp_index+1) + '.txt'), 'a')
	abstract_id_log.write(abstract_input_tag_id)
	abstract_id_log.write('\n')
	abstract_id_log.close()

def abstract_date_scraper(title, abstract_soup, status_logger_name):
	# Scrapes the date associated with each of the abstracts
	date_scraper_entry_status_key = "Scraping date of the abstract titled: " + title
	status_logger(status_logger_name, date_scraper_entry_status_key)

	try:
		abstract_date = abstract_soup.find('time').get('datetime')
		date_scraper_exit_status_key = title + " was published on " + abstract_date
	except AttributeError:
		abstract_date = "Date for abstract titled: " + title + " was not available"
		date_scraper_exit_status_key = abstract_date
		pass

	status_logger(status_logger_name, date_scraper_exit_status_key)

	return abstract_date

def abstract_scraper(abstract_soup):
	# Scrapes the abstract from the soup and returns to the page scraper
	abstract = str(abstract_soup.find('div', {'id':'Abs1-content'}).text.encode('utf-8'))[1:]

	return abstract

def author_scraper(abstract_soup, status_logger_name):
	# Scrapes the author of the text, for easy navigation and search
	author_scraper_start_status_key = "Scraping the author name"
	status_logger(status_logger_name, author_scraper_start_status_key)

	# Converts author names to a findAll() list and then concatinates into a string for storage
	author = ''.join(str(author) for author in [authorElement.text 
	for authorElement in abstract_soup.findAll('li', {'class':'c-article-author-list__item'})])

	author_scraper_end_status_key = "Scraped the author's name: " + str(author)
	status_logger(status_logger_name, author_scraper_end_status_key)

	return author

def title_scraper(abstract_soup, status_logger_name):
	# Scrapes the title of the text from the abstract
	title_scraper_start_status_key = "Scraping the title of the abstract"
	status_logger(status_logger_name, title_scraper_start_status_key)
	
	# Retrieves the title of the text even if an AttributeError arises
	try:
		title = str(abstract_soup.find('h1', {'class':'c-article-title'}).text.encode('utf-8'))[1:]
		# In case title is mislabeled, check more of publication for title tag
	except AttributeError:
		try:
			title = str(abstract_soup.find('h1',{'class':'ChapterTitle'}).text.encode('utf-8'))[1:]
		except AttributeError:
			try:
				title = (abstract_soup.find('span', {'class':'JournalTitle'}).text)
			except AttributeError:
				title = "Title not available"

	title_scraper_end_status_key = "Scraped the title of the abstract"
	status_logger(status_logger_name, title_scraper_end_status_key)
	
	return title

def abstract_id_scraper(abstract_id_log_name, page_soup, site_url_index, status_logger_name):
	# Obtains ID PII number of abstract
	abstract_id_scraper_start_status_key = "Scraping IDs"
	status_logger(status_logger_name, abstract_id_scraper_start_status_key)
	
	# Collects all tags with IDs in them
	abstract_input_tags = page_soup.findAll('a', {'class':'title'})
	for abstract_input_tag in abstract_input_tags:
		abstract_input_tag_id=abstract_input_tag.get('href')
		abstract_id_database_writer(abstract_id_log_name, abstract_input_tag_id, site_url_index)

	abstract_id_scraper_stop_status_key = "Scraped IDs"
	status_logger(status_logger_name, abstract_id_scraper_stop_status_key)

def word_sorter_list_generator(status_logger_name):
	word_sorter_list_generator_start_status_key = "Generating the permanent archival list"
	status_logger(status_logger_name, word_sorter_list_generator_start_status_key)
	
	# List holding words that correspond to abstract data
	word_sorter_list = []

	word_sorter_list_generator_exit_status_key = "Generated the permanent archival list"
	status_logger(status_logger_name, word_sorter_list_generator_exit_status_key)
	
	return word_sorter_list

def delay_function(status_logger_name):
	# Reduces number of pings sent to Springer servers in case of server issues

	delay_variable = np.random.randint(0, 20)

	delay_function_start_status_key = "Delaying remote server ping: " + str(delay_variable) + " seconds"
	status_logger(status_logger_name, delay_function_start_status_key)

	# Delays code by 1 second(s)
	time.sleep(delay_variable)

	delay_function_end_status_key = "Delayed remote server ping: " + str(delay_variable) + " seconds"
	status_logger(status_logger_name, delay_function_end_status_key)

def processor(abstract_url, urls_to_scrape, abstract_id_log_name, abstracts_log_name, status_logger_name, keywords_to_search):
	# Multiple page-cycling function to scrape multiple result pages returned from Springer.
	# print(len(urls_to_scrape))
	
	# List to hold all words mentioned in abstracts
	permanent_word_sorter_list = word_sorter_list_generator(status_logger_name)

	for site_url_index in range(0, len(urls_to_scrape)):
		# Collects the web-page from the url for scraping
		page_to_soup = url_reader(urls_to_scrape[site_url_index], status_logger_name)
		# Scraping the page for collection of data and tags
		page_soup = page_souper(page_to_soup, status_logger_name)
		# Scraping the page to extract all the abstract IDs
		abstract_id_scraper(abstract_id_log_name, page_soup, site_url_index, status_logger_name)
		# Obtains abstracts after combining ID with the abstract_url
		abstract_scanner(abstract_url, abstract_id_log_name, abstracts_log_name, 
        permanent_word_sorter_list, site_url_index, status_logger_name)
		# Delay after each page being scraped, rather than after each abstract
		delay_function(status_logger_name)

	# Dictionary generator for abstract data
	abstract_year_dictionary = abstract_year_list_post_processor(permanent_word_sorter_list, status_logger_name)

	return abstract_year_dictionary

def scraper_main(keywords_to_search, abstracts_log_name, status_logger_name):
	# Contains all functions and script to be used for calling scraper

	# Collect keywords created by user to begin scraping
	start_url, abstract_url, query_string = keyword_url_generator(keywords_to_search)

	# Extract abstract ID log name
	abstract_id_log_name =  abstract_id_log_name_generator(abstracts_log_name)

	if(type(keywords_to_search) == str):
		# Used if code is ran as a function from a library
		keywords_to_search = argument_formatter(keywords_to_search)
	else:
		keywords_to_search = keywords_to_search

	# Provides links for the URLs to be scraped
	urls_to_scrape = url_generator(start_url, query_string, status_logger_name)

	# Calls the processor() function
	abstract_year_dictionary = processor(abstract_url, urls_to_scrape, abstract_id_log_name, 
    abstracts_log_name, status_logger_name, keywords_to_search)

    # Dumps the entire dictionary onto the disc for further analysis and inference
	abstract_year_dictionary_dumper(abstract_year_dictionary, abstracts_log_name, status_logger_name)

	return 0