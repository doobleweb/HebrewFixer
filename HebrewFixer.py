import sublime
import os
import re
import json
import sublime_plugin

# fixes mistypes from hebrew to english. (akuo => שלום)
# the plugin will replace all the letters to hebrew if most of the letters on the selection were in english, and vise versa.
class HebrewFixerCommand(sublime_plugin.TextCommand):

	# set global variables
	def _init_(self):
		relative_path = os.path.join(sublime.packages_path(), 'Hebrew Fixer')
		# gets the dictinary that maches each letter to its 
		self.dictionary = self.read_JSON(relative_path+'\LetterDictionary.json')
		self.revDictionary = self.reverseDictionary(self.dictionary)

	def run(self, edit):
		self._init_()

		# get all the selection
		sels = self.view.sel()

		#for each word selected, switchs the letter.
		for word in sels:
			self.view.replace(edit, word, self.fixString(self.view.substr(self.view.word(word))))

	def fixString(self, str):
		newStr = ''
		mostlyEnglish = self.isMostlyEnglish(str)
		print('in fix string')
		
		if mostlyEnglish:
			searchDictionary = self.dictionary
		else:
			searchDictionary = self.revDictionary

		for x in range(len(str)):
			if(str[x] in searchDictionary):
				newStr += searchDictionary[str[x]]
			else:
				newStr += str[x]
		return newStr

	# checks if there are more english letters then hebrew ones on the given string
	def isMostlyEnglish(self, str):
		return len(re.findall(r'[a-zA-Z]', str)) > len(re.findall(r'[א-ת]', str))

	# reverse the dictionary so the change from hebrew to english will be easier;
	def reverseDictionary(self, dic):
		return dict (zip(dic.values(),dic.keys())) 

	# get the content of a json file into a dictionary object
	def read_JSON(self, path):
		""" read json file from the given path """
		with open(path, encoding="utf8") as json_file:
			try:
				data = json.load(json_file)
			except Exception as e:
				data = {}
				sublime.active_window().status_message("hebrew fixer had an error")
				print(str(e))
			return data