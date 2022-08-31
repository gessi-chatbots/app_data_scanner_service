import itertools
import requests

from flask import current_app

class Utils:

	def rotateAlternativeToNames(name, head, tail, context):

		#context.logger.info("Looking for all AlternativeTo name possibilities for " + name)

		whitespaced_names = name.split(' ')
		names = []
		#https://stackoverflow.com/questions/464864/how-to-get-all-possible-combinations-of-a-list-s-elements
		for L in range(0, len(whitespaced_names)+1):
			for subset in itertools.combinations(whitespaced_names, L):
 				if (len(subset) > 0):
 					names.append("".join(subset))
		
		success = False
		i = 0
		url = ""
		while not success and i < len(names):
		    url = head + names[i] + tail
		    req = requests.get(url)
		    if req.status_code != 404:
		        success = True
		    else:
		        i += 1

		if success:
			#context.logger.info("Success! " + url)
			return success, req
		else:
			#current_app.logger.info("No option was found")
			return success, None