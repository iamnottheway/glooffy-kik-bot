import time
import random
from flask import Flask, request, Response,render_template
from kik import KikApi, Configuration
from kik.messages import messages_from_json,TextMessage
#from tag_speech import SpeechTagger
# import responses
from responses import UsrgreetingList,messageList,help_str
from weather_request import *
from wit import Wit

bot = Wit(access_token="VOCFYQI6MHUL7CDRMPURE4Z26KJGNL7G")

usr_name = 'glooffybot'
key = '71981fb3-c57d-43bf-ac84-534120e8857e'
weather_key = "396cbf110cc7bd1bd3087f317643a83f"

app = Flask(__name__)
kik = KikApi(usr_name, key)

# this is for the kik server. It sets up the webhook so that kik server can
# send messages to the webhook and then incoming function extracts the data
# recieved.
kik.set_configuration(Configuration(webhook='https://glooffy.herokuapp.com/'))

def SendMessage(user,ch_id,msg):
	# sends a single message
	kik.send_messages([TextMessage(to=user,chat_id=ch_id,body=msg)])

@app.route('/', methods=['POST'])
def incoming():
	if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
		return Response(status=403)

    # list of python objects
	messages = messages_from_json(request.json['messages'])
	user_name = messages[0].from_user
	chatting_id = messages[0].chat_id
	current_msg = messages[0].body.lower()

    # store the user info
	c_user = kik.get_user(user_name)
    # user messages
    #SendMessage(user_name,chatting_id,help_str)
	resp = bot.message(current_msg)
	entity = "#other"
	try:
		entity = list(resp['entities'])[0]
		try:
			# store the location if available
			location_entity = list(resp['entities'])[1]
			# get the location name
			location = resp['entities']['location'][0]['value']
		except:
			pass
	except:
		pass
	if entity == "greetings":
		greeting_list = ["hey-o","Yo","Hi-yo","me cool, you?","hi","hey"]
		SendMessage(user_name,chatting_id,greeting_list[random.randint(0,len(greeting_list)-1)])
	elif entity == "fine_tag":
		fine_resp = ["That's great!","Nice!","Cool, Human!","good to know"]
		SendMessage(user_name,chatting_id,fine_resp[random.randint(0,len(fine_resp)-1)])
	elif entity == "ask_fine":
		ask_fine_resp = ["Yeah me cool!","I'm cool!","I'm well","yeah, I'm awesome!","I'm fine"]
		SendMessage(user_name,chatting_id,ask_fine_resp[random.randint(0,len(ask_fine_resp)-1)])
		# get the weather
	elif entity == "get_weather":
		# if location is available get the weather with location, else
		# get the weather of the current place
		SendMessage(user_name,chatting_id,"Wait a sec...")
		try:
			SendMessage(user_name,chatting_id,"here's the weather")
			wex = WexExtractor(location,weather_key)
			data = wex.GetJsonData()
			weather_msg = data['weather'][0]['description']
			SendMessage(user_name,chatting_id,weather_msg)
		except:
			SendMessage(user_name,chatting_id,"current location weather")

	else:
		SendMessage(user_name,chatting_id,"Sorry, didn't catch that!")
	return Response(status=200)

@app.route('/')
def show_index_page():
	return render_template("index.html")


if __name__ == "__main__":
	app.run(port=8080, debug=True)
