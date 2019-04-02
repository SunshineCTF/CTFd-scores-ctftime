from flask import jsonify, request

from CTFd import utils
from CTFd.utils.config.visibility import scores_visible
from CTFd.utils.scores import get_standings


def load(app):
	# Implement the JSON API format that ctftime expects
	@app.route("/scores", methods=["GET"])
	def scores():
		json = {'standings': []}
		
		# Check if the user can view scores, otherwise return empty JSON response
		if not scores_visible():
			return jsonify(json)
		
		# Look up the standings from the database
		standings = get_standings()
		
		# Fill the standings into the JSON object, assigning each team a rank
		for i, x in enumerate(standings):
			json['standings'].append({'pos': i + 1, 'id': x.account_id, 'team': x.name, 'score': int(x.score)})
		
		return jsonify(json)
