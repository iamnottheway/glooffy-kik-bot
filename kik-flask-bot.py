import time
import random
from flask import Flask, request, Response
from kik import KikApi, Configuration
from kik.messages import messages_from_json,TextMessage
from tag_speech import SpeechTagger

# import responses
from responses import UsrgreetingList,messageList,help_str


usr_name = 'spencethepetbot'
key = '3866b0c5-7ac3-49a2-9f29-ed3b27fbd5b1'

app = Flask(__name__)
kik = KikApi(usr_name, key)

kik.set_configuration(Configuration(webhook='http://c0a2c220.ngrok.io'))

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
	if current_msg in UsrgreetingList:
		SendMessage(user_name,chatting_id,messageList[random.randint(0,len(messageList)-1)])
	elif current_msg == "help":
		SendMessage(user_name,chatting_id,help_str)
	else:
		tag_speech = SpeechTagger()
		chat_response = tag_speech.look_and_tag(current_msg)
		SendMessage(user_name,chatting_id,chat_response)
	return Response(status=200)
    


if __name__ == "__main__":
	app.run(port=8080, debug=True)
