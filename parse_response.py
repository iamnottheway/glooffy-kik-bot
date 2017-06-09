# parse the user response 
import re

class ParseUserResponse():

	# split the response and try to look for key words
	# in the user response, so that the bot can give relevant 
	# response to the user.
	# IF a match is found then launch an action function

	def __init__(self):
		self.PetSh1 = r"near[a-z]* pet store|petshop|get [a-z]* pet"#order or request type
		self.res1 = re.findall(self.PetSh1,"get me the nearest petshop")
		print(self.res1)

par = ParseUserResponse()