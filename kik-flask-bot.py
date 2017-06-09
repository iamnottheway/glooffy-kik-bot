import time
import random
from flask import Flask, request, Response
from kik import KikApi, Configuration
from kik.messages import messages_from_json,TextMessage


usr_name = ''
key = ''

app = Flask(__name__)
kik = KikApi(usr_name, key)

kik.set_configuration(Configuration(webhook=''))

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
	UsrgreetingList = ["hi","hey","sup","yo","wassup","hello"]
	for greet in UsrgreetingList:
		if current_msg == greet:
			messageList = ["Hello, what's up? {}🌊!".format(c_user.first_name),\
			"Yo, woof woof {}🌻!".format(c_user.first_name),\
			"🐶🌻🌴🌊 woooofff wooofff!!",\
			"hey {}".format(c_user.first_name),\
			"welcome back!"]
			SendMessage(user_name,chatting_id,messageList[random.randint(0,len(messageList)-1)])
		elif current_msg == 'help':
			help_str = """
			I can...🐶\n
			1) Show you all the pet stores in your city or anywhere in the world🌎\n
			2) name your pet for you🎂\n
			3) play a game with you🎲\n
			4) Inspire you
			"""
			SendMessage(user_name,chatting_id,help_str)
			break
		else:
			# just send one message
			SendMessage(user_name,chatting_id,"Yo, i'm a dog. My speech is limited. Type 'help' 🐶")
			break
	return Response(status=200)
    


if __name__ == "__main__":
	app.run(port=8080, debug=True)
