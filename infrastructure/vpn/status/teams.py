import requests
import json

USE_REAL_TEAMS = True

URL = "http://ructf.org/e/2014/teams/info"

def get_teams():
	teams = {}
	if not USE_REAL_TEAMS:
		for i in range(768):
			teams[i] = "test_team%d" % i
	else:
		content = requests.get(URL).text
		teams_list = json.loads(content)
		for team_id, team_name in teams_list:
			if type(team_id) is int:
				teams[team_id] = team_name
	return teams
