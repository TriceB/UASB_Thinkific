"""
    Scoreboard for UA Students Course completion

    -  Things that need to be done

    Connect  School goal to Add your Own

    Connect to Thinkific API to find Affiliate Cash

    The order Endpoint needs to tied to Affiliate code

    GetOrder

    - Affiliate Referral code

    Get Users

    Affiliate Code

    Amount of commission

    20% of $20
"""

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
    get_affiliate_members()
    pprint(list_of_affiliate_members)
    affiliate_members_json = json.dumps(list_of_affiliate_members, indent=4)
    with open("affiliate_members.json", "w") as affiliate_members_file:
        affiliate_members_file.write(affiliate_members_json)
        affiliate_members_file.close()
    

list_of_affiliate_members = []


def get_affiliate_members(page_num=1):
    """
    This function will access the Thinkific API and get all of the members currently enrolled in Unlock Academy
    """
    # page_num = 1
    params = (
        ('page', page_num),  # page_num
        # as of 9/21 there are a total of 17962 users
        # as of 11/7 there are a total of 18261 users
        ('limit', '1000')
        # ('limit', '100')
    )

    response = requests.get('https://api.thinkific.com/api/public/v1/users', headers=headers, params=params)
    members_response = response.text.encode('utf8')
    members_parsed = json.loads(members_response)
    members = members_parsed["items"]
    # pprint(members_parsed)
    current_page = members_parsed["meta"]["pagination"]["current_page"]
    # print("CURRENT PAGE = ", current_page)
    next_page = members_parsed["meta"]["pagination"]["next_page"]
    # print("NEXT PAGE = ", next_page)
    total_pages = members_parsed["meta"]["pagination"]["total_pages"]
    total_items = members_parsed["meta"]["pagination"]["total_items"]
    # print("TOTAL ITEMS = ", total_items)
    # print("TOTAL PAGES = ", total_pages)
    # print("MEMBERS PARSED")
    # pprint(members_parsed)
    # print("NEXT PAGE IS " + str(next_page))
    # pprint(next_page)
    members_df = pd.json_normalize(members_parsed,
                                   record_path=['items'],
                                   meta=["roles"],
                                   meta_prefix='meta-',
                                   errors='ignore')
    # for member in members_df:
    #     print("MEMBER here")
    #     pprint(member)
        # if 'affiliate' in members_df:
        #     pprint(member)
    for member in members_parsed['items']:
        # test_member = member
        # print(f" test member {member['roles']}")
        # pprint(len(member))
        if 'affiliate' in member['roles']:
            # print(f" test member {member['roles']}")
            # member_name_split = member["name"].split(maxsplit=1)
            # if len(member_name_split) > 1:
            #     member_first_name = member_name_split[0]
            #     member_last_name = member_name_split[1]
            member = {"email": member["email"],
                      "first_name": member["first_name"],
                      "last_name": member["last_name"],
                      "student_id": member["id"],
                      "affiliate_code": member["affiliate_code"],
                      "affiliate_commission": member["affiliate_commission"],
                      "affiliate_commission_type": member["affiliate_commission_type"],
                      "affiliate_payout_email": member["affiliate_payout_email"],
                      "roles": member['roles']
                      }
            list_of_affiliate_members.append(member)

    if current_page != total_pages:
        page_num += 1
        get_affiliate_members(page_num)
    else:
        print("The End of get_affiliate_members()")

    return list_of_affiliate_members


# list_thinkific_courses = []


# def get_thinkific_courses(page_num=1):
#     params = (
#         ('page', page_num),  # page_num
#         # ('limit', '50000')
#         # ('limit', '200')
#     )
#     response = requests.get(
#         'https://api.thinkific.com/api/public/v1/courses?',
#         headers=headers,
#         params=params)
#     courses_response = response.text.encode('utf8')
#     courses_parsed = json.loads(courses_response)
#     courses = courses_parsed["items"]
#     current_page = courses_parsed["meta"]["pagination"]["current_page"]
#     # print("CURRENT PAGE = ", current_page)
#     next_page = courses_parsed["meta"]["pagination"]["next_page"]
#     # print("NEXT PAGE = ", next_page)
#     total_pages = courses_parsed["meta"]["pagination"]["total_pages"]
#     total_items = courses_parsed["meta"]["pagination"]["total_items"]
#     # print("TOTAL ITEMS = ", total_items)
#     # print("TOTAL PAGES = ", total_pages)

#     for course in courses:
#         course_info = {"course_name": course["name"],
#                        "course_id": course["id"],
#                        "course_instructor": course["instructor_id"]
#                        }
#         list_thinkific_courses.append(course_info)

#     if current_page != total_pages:
#         page_num += 1
#         get_thinkific_courses(page_num)
#     else:
#         print("The End of get_thinkific_courses")
#     return list_thinkific_courses


# list_of_student_enrollments = []


# def get_student_enrollments(page_num=1):  # page_num=1
#     """
#     Function to get all Students and the classes they are enrolled in
#     """

#     # page_num = 1
#     params = (
#         ('page', page_num),  # page_num
#         # ('limit', '50000')
#         ('limit', '1000')
#     )
#     response = requests.get(
#         'https://api.thinkific.com/api/public/v1/enrollments?',
#         headers=headers,
#         params=params)
#     students_response = response.text.encode('utf8')
#     students_parsed = json.loads(students_response)
#     students = students_parsed["items"]
#     current_page = students_parsed["meta"]["pagination"]["current_page"]
#     # print("CURRENT PAGE = ", current_page)
#     next_page = students_parsed["meta"]["pagination"]["next_page"]
#     # print("NEXT PAGE = ", next_page)
#     total_pages = students_parsed["meta"]["pagination"]["total_pages"]
#     total_items = students_parsed["meta"]["pagination"]["total_items"]
#     # print("TOTAL ITEMS = ", total_items)
#     # print("TOTAL PAGES = ", total_pages)

#     for student in students:
#         student_email = student["user_email"].lower()
#         student_name_split = student["user_name"].split(maxsplit=1)

#         course_start_date = student["started_at"]
#         course_completion_date = student["completed_at"]
#         # print("Course Start Date - ", course_start_date, "
#         # Completion Date - ", course_completion_date)

#         if isinstance(course_start_date, str):
#             start_date_format = '%Y-%m-%dT%H:%M:%S.%f%z'
#             course_start_date = datetime.strptime(
#                 course_start_date,
#                 start_date_format)
#             # print("Course Start Date - ", course_start_date)

#         if isinstance(course_completion_date, str):
#             completion_date_format = '%Y-%m-%dT%H:%M:%S.%f%z'
#             course_completion_date = datetime.strptime(
#                 course_completion_date,
#                 completion_date_format)
#             # print("Completion Date - ", course_completion_date)

#         if len(student_name_split) > 1:
#             student_first_name = student_name_split[0]
#             student_last_name = student_name_split[1]
#             student_info = {"email": student_email,
#                             "first_name": student_first_name,
#                             "last_name": student_last_name,
#                             "course_name": student["course_name"],
#                             "course_id": student["course_id"],
#                             "course_started": course_start_date,
#                             "completion_status": student["completed"],
#                             "percentage_completed": student["percentage_completed"],
#                             "date_completed": course_completion_date
#                             }
#             list_of_student_enrollments.append(student_info)
#         else:
#             student_first_name = student_name_split[0]
#             student_info = {"email": student_email,
#                             "first_name": student_first_name,
#                             "course_name": student["course_name"],
#                             "course_id": student["course_id"],
#                             "course_started": course_start_date,
#                             "completion_status": student["complete"],
#                             "percentage_completed": student["percentage_completed"],
#                             "date_completed": course_completion_date
#                             }
#             list_of_student_enrollments.append(student_info)

#     if current_page != total_pages:
#         page_num += 1
#         get_student_enrollments(page_num)

#     else:
#         print("The End of get_student_enrollments()")

#     return list_of_student_enrollments


if __name__ == "__main__":
    main()
