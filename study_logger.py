'''This script accepts a command line argument as subject name,
stores it in a csv with the start time and when ended via another
command line call will stop the logging and add the stop time

Dependencies:
	buffer memory - for monitoring latest task
	csv database - schema : subject name, start time, end time, duration
'''

import argparse
import csv
import os
import datetime as dt
import time
from organize_file import manage_file
import pathlib
import configparser as cfg

config = cfg.ConfigParser(interpolation=cfg.ExtendedInterpolation())
config.read('study_logger.ini')

csv_data_proxy = config['csv_data']
csv_metadata_proxy = config['csv_metadata']

# logging.basicConfig(level=logging.INFO)


#create database if it does not already exist
data_dir = csv_metadata_proxy.get('rootdir')
csv_filename = csv_metadata_proxy.get('base_filename')
timestamp_style = csv_metadata_proxy.get('timestamp_style')
file_path = os.path.join(data_dir, csv_filename)
path_obj = pathlib.Path(file_path)
file_parent, file_stem, file_suffix = str(path_obj.parent), path_obj.stem, path_obj.suffix

#the below method takes care of parent directories existence no matter how deeply nested it is
organized_csv_filename = manage_file(file_parent, file_stem, file_suffix, add_time = False, categorize_by_day = True)

csv_fieldnames = csv_data_proxy.get('fields').split(',')
#check whether base file already exists or not
if not os.path.exists(organized_csv_filename):
	with open(organized_csv_filename, 'w') as csvfile:
		csv_writer = csv.DictWriter(csvfile, fieldnames = csv_fieldnames)
		csv_writer.writeheader()


argparser = argparse.ArgumentParser()
#adding optional argument
argparser.add_argument('-s', '--subject', required=True, help = 'Name of subject that user is currently engaged in')
argparser.add_argument('duration_in_mins', type = float)

args = argparser.parse_args()

subject_name = args.subject
duration_set = args.duration_in_mins
#date object
start_time = dt.datetime.now()

#row values
rowvals = [subject_name, start_time]
# csv_rowdict = dict(zip(csv_fieldnames[:2], rowvals))
# with open(csv_filename, 'a+') as csvfile:
# 	csv_writer = csv.DictWriter(csvfile, fieldnames = csv_fieldnames)
# 	csv_writer.writerow(csv_rowdict)

time_str = start_time.strftime(timestamp_style)
#print information
print(f'Started learning {subject_name.upper()} at {time_str}...')
print('All timedelta are in minutes')
time_counter = 0

print('Time elapsed in minutes : ')
while True:
	#if study begins
	try:
		#start counter
		time_counter += 1
		time.sleep(1)
		print(f'{round(time_counter/60, 1)} ', end = '\r')

		
	except KeyboardInterrupt as ki:
		end_time = dt.datetime.now()
		duration = end_time - start_time
		#converting duration into minutes
		duration = round(duration.seconds/60)
		met_milestone = duration >= duration_set
		percent_met = round((duration/duration_set) * 100, 1)
		rowvals.extend([end_time, duration, duration_set, met_milestone, percent_met])
		csv_rowdict = dict(zip(csv_fieldnames, rowvals))
		with open(organized_csv_filename, 'a+') as csvfile:
			csv_writer = csv.DictWriter(csvfile, fieldnames = csv_fieldnames)
			csv_writer.writerow(csv_rowdict)
		end_time_str = end_time.strftime(timestamp_style)
		total_time_elapsed = end_time - start_time 
		print(f'Study completed at {end_time_str}')
		print(f'Total time elapsed : {total_time_elapsed.seconds//60} minutes')
		break