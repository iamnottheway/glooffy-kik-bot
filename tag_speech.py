# simple-speech tagger : tags the sentence with relevent speech tags
# Each sentence has it's own intent and it's difficult to know the
# intent for everything the user says. If the input is irrelevent to the context
# that is weather, add a tag as #other_stuff. Then use some online api to make small talk

'''
This is not a sophisticated nlp speech tagger!
simple speech tagger works by:

	> validation the input
	> looking for relevent key_words
	> tagging em'


'''

from nltk.corpus import stopwords

import re


def remove_stopwords(input_str):
	stop = set(stopwords.words('english'))
	return [i for i in input_str.lower().split() if i not in stop]


class SpeechTagger():

	def __init__(self):
		pass

	def validate_input(self,input_text):
		'''
		validate_input() normalizes the input and removes any punctuations.
		If the string is empty, marks it as false

		'''
		self.input_text = input_text
		validation_check = False
		# if the string is not empty then do validaion and return string.
		# else return validation_check = False
		if self.input_text is not '' or self.input_text is not empty:
			self.input_text = self.input_text.lower()[0:-1]
			self.input_text = remove_stopwords(self.input_text)
			return self.input_text
		return validation_check

	def look_and_tag(self,tag_string):
		self.init_str = tag_string
		# validation is done for tagging only
		self.tag_string	= self.validate_input(tag_string)
		# tagged string contains string and tag
		self.tagged_string = [[None,None]]
		self.tag_validators = [
							"#current_weather","#current_temperature",
							"#current_time","current_location",
							"#greetings","#goodbyes",
							"#other_stuff","#what_you_sayin_bro"
						]
		if "weather" in self.tag_string:
			self.tagged_string[0][0] = self.init_str
			self.tagged_string[0][1] = self.tag_validators[0] # tag with weather
		elif "hot" or "cold" or "freezing" or "melting" or "temperature" in self.tag_string:
			self.tagged_string[0][0] = self.init_str
			self.tagged_string[0][1] = self.tag_validators[1] # tag with weather
		else:
			self.tagged_string[0][0] = self.init_str
			self.tagged_string[0][1] = self.tag_validators[-2] # tag with other_stuff
		return self.tagged_string



sp = SpeechTagger()
test_list = [
			"what is the weather in London","is it hot in london",
			"is it cold in london","is it freezing in the arctic",
			"is it melting in africa","blah",
			"i want a dog","weather in london"
]

for t_str in  test_list:
	y = sp.look_and_tag(t_str)
	print(y)

















