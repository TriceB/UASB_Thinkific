"""
Need to find out how many courses a student has completed

"""
import collections
import requests
import pandas as pd
import json
import os
from pprint import pprint, pformat
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, date
import time
from pprint import pprint

headers = {
	'accept': 'application/json',
	'X-Auth-API-Key': os.environ.get('THINKIFIC_API_KEY'),
	'X-Auth-Subdomain': os.environ.get('THINKIFIC_SUBDOMAIN')
	}


def main():
	get_student_enrollments()
	pprint(list_of_student_enrollments)
	calculate_courses_completed()


list_of_student_enrollments = []


def get_student_enrollments(page_num=1):  # page_num=1
	"""
	Function to get all Students and the classes they are enrolled in
	"""
	
	# page_num = 1
	params = (
		('page', page_num),  # page_num
		# ('limit', '50000')
		('limit', '1000')
		)
	response = requests.get('https://api.thinkific.com/api/public/v1/enrollments?', headers=headers, params=params)
	students_response = response.text.encode('utf8')
	students_parsed = json.loads(students_response)
	students = students_parsed["items"]
	current_page = students_parsed["meta"]["pagination"]["current_page"]
	# print("CURRENT PAGE = ", current_page)
	next_page = students_parsed["meta"]["pagination"]["next_page"]
	# print("NEXT PAGE = ", next_page)
	total_pages = students_parsed["meta"]["pagination"]["total_pages"]
	total_items = students_parsed["meta"]["pagination"]["total_items"]
	# print("TOTAL ITEMS = ", total_items)
	# print("TOTAL PAGES = ", total_pages)
	
	for student in students:
		student_email = student["user_email"].lower()
		student_name_split = student["user_name"].split(maxsplit=1)
		
		course_start_date = student["started_at"]
		course_completion_date = student["completed_at"]
		# print("Course Start Date - ", course_start_date, "Completion Date - ", course_completion_date)
		
		if isinstance(course_start_date, str):
			start_date_format = '%Y-%m-%dT%H:%M:%S.%f%z'
			course_start_date = datetime.strptime(course_start_date, start_date_format)
		# print("Course Start Date - ", course_start_date)
		
		if isinstance(course_completion_date, str):
			completion_date_format = '%Y-%m-%dT%H:%M:%S.%f%z'
			course_completion_date = datetime.strptime(course_completion_date, completion_date_format)
		# print("Completion Date - ", course_completion_date)
		if student["percentage_completed"] == "1.0":
			if len(student_name_split) > 1:
				student_first_name = student_name_split[0]
				student_last_name = student_name_split[1]
				student_info = {student["id"]: int(float(student["percentage_completed"])),
				                "student_id": student["id"],
				                "email": student_email,
				                "first_name": student_first_name,
				                "last_name": student_last_name,
				                "course_name": student["course_name"],
				                "course_id": student["course_id"],
				                "course_started": course_start_date,
				                "completion_status": student["completed"],
				                "percentage_completed": student["percentage_completed"],
				                "date_completed": course_completion_date
				                }
				list_of_student_enrollments.append(student_info)
			else:
				student_first_name = student_name_split[0]
				student_info = {student["id"]: int(float(student["percentage_completed"])),
				                "student_id": student["id"],
				                "email": student_email,
				                "first_name": student_first_name,
				                "course_name": student["course_name"],
				                "course_id": student["course_id"],
				                "course_started": course_start_date,
				                "completion_status": student["complete"],
				                "percentage_completed": student["percentage_completed"],
				                "date_completed": course_completion_date
				                }
				list_of_student_enrollments.append(student_info)
	
	if current_page != total_pages:
		page_num += 1
		get_student_enrollments(page_num)
	
	else:
		print("The End of get_student_enrollments()")
	
	return list_of_student_enrollments


def calculate_courses_completed():
	courses_completed_per_student = collections.Counter()
	total_courses_completed = 0
	for course_completed in list_of_student_enrollments:
		
		print(course_completed)
		courses_completed_per_student.update(course_completed)
		
		for course in course_completed:
			total_courses_completed = int(course_completed[course]) + total_courses_completed
			
			print(total_courses_completed)
	
	courses_completed_per_student = dict(courses_completed_per_student)
	print(courses_completed_per_student)


if __name__ == "__main__":
	main()
