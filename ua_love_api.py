"""
Test Page (renders index.html) to check for functionality for the message board - seems like coach has a SQL database
where everything
will be stored
Storing test messages in JSON for now
"""

from flask import Flask, render_template, request
import json
from datetime import datetime

app = Flask(__name__)

message_information = []


@app.route('/', methods=["GET", "POST"])
def send_message():
	"""
	This will display the message box where a student can leave a new message
	
	"""
	test = "this is a test"
	if request.method == "POST" and request.form.get('action') == "Add A Message":
		
		# store all of the user inputs into variables
		# TODO: update this after connecting the Thinkific API to get the actual Tribe student ID and Name
		student_id = '123456'
		student_name = request.form.get('studentName')
		student_message = request.form.get('studentMessage')
		message_date_time = datetime.now()
		
		# turn the datetime into a datetime object in the format of the timestamp
		full_date_time_object = message_date_time.strftime('%d %b %Y %H:%M')
		
		# concatenate the student_id with the date and time of the message sent, to generate a message id
		# TODO: find out if Coach is planning to generate his own unique message id in a different way
		#  could use random number generator but this would generate a new number each time the program runs
		message_id = student_id + '_' + full_date_time_object
		if student_message:
			try:
				# put all of formatted message information into a dict to append to message_information list
				message_information_dict = {'ua_student_id': student_id,
				                            'ua_student_name': student_name,
				                            'message': student_message,
				                            'timestamp': full_date_time_object,
				                            'message_id': message_id
				                            }
				message_information.append(message_information_dict)
				
				# format the list of messages into json with 4 indent spaces for easier readability
				message_json = json.dumps(message_information, indent=4)
				
				# write all of the message submissions to the json file
				# this file will get overridden each time the flask app is run to
				# keep only the current set of messages
				with open("messages.json", "w") as messages_file:
					messages_file.write(message_json)
					messages_file.close()
			
				return render_template("index.html",
				                       student_id=student_id,
				                       student_name=student_name,
				                       student_message=student_message,
				                       full_date_time_object=full_date_time_object,
				                       message_id=message_id)
			except ValueError:
				no_message_error = "Enter some love for your fellow Tribe Member"
				return render_template("index.html",
				                       no_message_error=no_message_error)
	
	return render_template("index.html", test=test)


if __name__ == '__main__':
	app.run(debug=True)
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
