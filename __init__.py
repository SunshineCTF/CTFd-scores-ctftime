from flask import jsonify, request

from CTFd.models import Teams
from CTFd.utils.config.visibility import scores_visible
from CTFd.utils.scores import get_standings
from CTFd.utils.challenges import get_all_challenges
from CTFd.utils.dates import unix_time

def load(app):
	# Implement the JSON API format that ctftime expects
	@app.route("/scores", methods=["GET"])
	def scores():
		json = {'standings': []}
		
		# Check if the user can view scores, otherwise return empty JSON response
		if not scores_visible():
			return jsonify(json)
		
		challenges = get_all_challenges()

		value_lookup = {}
		name_lookup = {}
		for challenge in challenges:
			value_lookup[challenge.id] = challenge.value
			name_lookup[challenge.id] = challenge.name

		# Look up the standings from the database
		standings = get_standings()

		# Fill the standings into the JSON object, assigning each team a rank
		for i, x in enumerate(standings):
			# For each account, get the timing of each solve
			team = Teams.query.filter_by(id=x.account_id).first_or_404()
			solves = team.get_solves()

			formatted_solves = {
				f'{name_lookup[s.challenge_id]}': { "time": unix_time(s.date), "points": value_lookup[s.challenge_id] } for s in solves
			}

			last_accept = max([unix_time(s.date) for s in solves], default=None)
			json['standings'].append({'pos': i + 1, 'id': x.account_id, 'team': x.name, 'score': int(x.score), 'taskStats': formatted_solves, 'lastAccept': last_accept })

		json['tasks'] = [
			challenge.name for challenge in challenges
		]

		return jsonify(json)
