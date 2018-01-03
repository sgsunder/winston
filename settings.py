import json

# Simple class to store settings, uses JSON file for permanance
class Settings:
	def __init__(self):
		self._path = "settings.json"
		self._tokenpath = "token"
		self._settings = self._load_settings()

		self.token = self._load_token()

		self.admin_role = self._settings["admin role"]
		self.mod_role = self._settings["mod role"]
		self.prefix = self._settings["prefix"]
		self.roles = self._settings["roles"]

	# Loads Class Variables from JSON file
	def _load_settings(self):
		file = open(self._path, "r")
		data = json.loads(file.read())
		file.close()

		return data

	# Dumps Current Class Variables to JSON file
	def _save_settings(self):
		settings_string = json.dumps(self._settings, sort_keys=True, indent=4, separators=(",", ": "))
		file = open(self._path, "w")
		file.write(settings_string)
		file.close()

	# Changes a setting and updates JSON file
	def change_setting(self, setting, new_setting):
		self._settings[setting] = new_setting
		self._save_settings()
		self._load_settings()

	# Loads the Discord API Token from a seperate file
	def _load_token(self):
		file = open(self._tokenpath, "r")
		data = file.read().replace('\n', '')
		file.close()

		return data

settings = Settings()
