import json

class Settings:
	def __init__(self):
		self._path = "settings.json"
		self._settings = self._load_settings()
		
		self.admin_role = self._settings["admin role"]
		self.mod_role = self._settings["mod role"]
		self.prefix = self._settings["prefix"]
		self.roles = self._settings["roles"]
		self.token = self._settings["token"]
	
	def _load_settings(self):
		file = open(self._path, "r")
		settings = json.loads(file.read())
		file.close()
		
		return settings
	
	def _save_settings(self):
		settings_string = json.dumps(self._settings, sort_keys=True, indent=4, separators=(",", ": "))
		file = open(self._path, "w")
		file.write(settings_string)
		file.close()
	
	def change_setting(self, setting, new_setting):
		self._settings[setting] = new_setting
		self._save_settings()
		self._load_settings()
	
settings = Settings()