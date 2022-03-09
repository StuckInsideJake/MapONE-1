# Functions used to enhance and simplify the processes occuring within the scraper class

# Importing datetime to track database logs w/ time values
from datetime import datetime
# Importing OS functions to build the LOG folders
import os
# Importing argparse to parse the keywords
import argparse

def status_logger(status_logger_name, status_key):
	# Status logger to print and log details of the program's output
	# Displays current hour, minute, and second
	current_hour = str(datetime.now().time().hour)
	current_minute = str(datetime.now().time().minute)
	current_second = str(datetime.now().time().second)

	# Logging and printing the complete_status_key
	complete_status_key = "[INFO]" + current_hour + ":" + current_minute + ":" + current_second + " " + status_key
	print(complete_status_key)
	status_log = open(status_logger_name + ".txt", "a")
	status_log.write(complete_status_key + "\n")
	status_log.close()

def status_logger_creator(abstracts_log_name):
	# Standalone status_logger and session_folder filename generator, if someone is using the components as standalone functions
	session_folder_name = abstracts_log_name.split("/")[-1]
	os.makedirs(session_folder_name)
	status_logger_name = session_folder_name + "/" + "Status_Logger"
	return status_logger_name, session_folder_name

def pre_processing(keywords):
	# Contains all the pre-processing statements related to the program's output
	# Includes Abstracts LOG Name, Status Logger Name

	if((type(keywords) == str)):
		# If the user uses the function independently of the argument_parser()
		# Needed to convert the keywords to a list of words
		keywords = argument_formatter(keywords)

	# Declaration of time and date variables
	run_start_year = str(datetime.now().date().year)
	run_start_month = str(datetime.now().date().month)
	run_start_day = str(datetime.now().date().day)
	run_start_date = str(datetime.now().date())
	run_start_hour = str(datetime.now().time().hour)
	run_start_minute = str(datetime.now().time().minute)
	run_start_second = str(datetime.now().time().second)

	# Keywords have to be written into the filename of the LOG that we are running
	folder_attachement = ""
	if(len(keywords) == 1):
		folder_attachement = keywords[0]
	else:
		for keyword_index in range(0, len(keywords)):
			if((keyword_index + 1) == len(keywords)):
				folder_attachement = folder_attachement+keywords[keyword_index]
			else:
				folder_attachement = folder_attachement+keywords[keyword_index] + "_"

	# Declaration of the LOG folder and the abstract, abstract_id & status_logger files
	logs_folder_name = "LOGS" + "/" + "LOG" + "_" + run_start_date + "_" + run_start_hour + "_" + run_start_minute + "_" + folder_attachement
	abstracts_log_name = logs_folder_name + "/" + "Abstract_Database" + "_" + run_start_date + "_" + run_start_hour + "_" + run_start_minute
	status_logger_name = logs_folder_name + "/" + "Status_Logger" + "_" + run_start_date + "_" + run_start_hour + "_" + run_start_minute

	# If the filename does not exist, create the file in the LOG directory
	if not os.path.exists(logs_folder_name):
		os.makedirs(logs_folder_name)
	
	# Creating the status_log and writing the session duration & date
	status_log = open(status_logger_name + '.txt', 'a')
	status_log.write("Session: " + run_start_day + "/" + run_start_month + "/" + run_start_year + "\n")
	status_log.write("Time: " + run_start_hour + ":" + run_start_minute + ":" + run_start_second + "\n")
	status_log.close()

	logs_folder_name_status_key = "Built LOG folder for session"
	status_logger(status_logger_name, logs_folder_name_status_key)

	return abstracts_log_name, status_logger_name

def keyword_url_generator(keywords_to_search):
	# Offloading some of the scraper specific functions to another function

	if((type(keywords_to_search) == str)):
		# If the user uses the function independently of the argument_parser()
		# Needed to convert the keywords to a list of words
		keywords = argument_formatter(keywords_to_search)

	query_string = ""
	if (len(keywords) == 1):
		query_string = keywords[0]
	else:
		for keyword_index in range(0, len(keywords)):
			if((keyword_index + 1) == len(keywords)):
				query_string = query_string + keywords[keyword_index]
			else:
				query_string = query_string + keywords[keyword_index] + "+"

	start_url = "https://link.springer.com/search/page/"
	abstract_url = 'https://link.springer.com'

	# Using the keywords, we generate the URLs here
	return start_url, abstract_url, query_string

def abstract_id_log_name_generator(abstracts_log_name):
	# Function to generate the abstract_id_log_name from the abstracts_log_name
	return abstracts_log_name.split('Abstract')[0] + 'Abstract_ID' + abstracts_log_name.split('Abstract')[1] + '_'

def argument_formatter(argument_string):
	# Function to split argument_string so we can use it across the pyResearchInsights stack
	return argument_string.split()

def arguments_parser():
	# Function used to read the initial keyword that will be queried in Springer (for now)
	# Scrapes Planetary Map Publications, using the following parameters:
	# a) --keywords: This argument is the term that will be searched for in Springer.
	# b) --trends: This argument provides the term whose research trend will be generated.

	parser = argparse.ArgumentParser()
	parser.add_argument("--keywords", help = "Keyword to search on Springer", default = "Mars")
	parser.add_argument("--trends", help = "Keywords to generate the trends histogram for", default = "Glaciers")

	# Parse the keyword if a string is split and then passed to the scraper functions
	arguments = parser.parse_args()
	if arguments.keywords:
		keywords = arguments.keywords

	keywords = argument_formatter(keywords)

	if arguments.trends:
		trends = arguments.trends

	trends = trends.lower()
	trends = argument_formatter(trends)

	return keywords, trends

def end_process(status_logger_name):
	# Declares successful completion of the code
	end_process_status_key = "Process has successfully ended"
	status_logger(status_logger_name, end_process_status_key)