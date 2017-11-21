class Context:
	def __init__(self, **attrs):
		self.args = attrs.pop("args", [])
		self.client = attrs.pop("client", None)
		self.command = attrs.pop("command", None)
		self.message = attrs.pop("message", None)
		self.prefix = attrs.pop("prefix", None)
		
		self.author = self.message.author
		self.channel = self.message.channel
		self.server = self.message.server
		self.text = self.message.content