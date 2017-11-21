import json

class Settings:
	def __init__(self):
		self._path = "settings.json"
		file = open(self._path)
		self._settings = json.loads(file.read())
		file.close()
		
		self.prefix = self._settings["prefix"]
		self.token = self._settings["token"]
settings = Settings()
