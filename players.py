import json

from player import Player

class Players:
	def __init__(self):
		self._path = "players.json"
		self.players = self._load_players()
	
	def _load_players(self):
		file = open(self._path)
		p_json = json.loads(file.read())
		file.close()
		
		def check(entry):
			if entry in p_json:
				return p_json[entry]
			else:
				return None
		
		players = []
		for id in p_json:
			players.append(Player(id, check("rank"), check("roles"), check("btag")))
		
		return players
	
	def _save_players(self):
		players_string = ""
		for player in self.players:
			players_string += json.dumps(player.__dict__, sort_keys=True, indent=4, separators=(",", ": "))
		
		file = open(self._path, "r")
		file.write(players_string)
		file.close()
	
	def add_player(self, player, btag=None, rank=None, roles=[]):
		pass
	
	def edit_player(self, player, rank, *roles):
		pass

players = Players()