from editor.common.database import Database


class Preference(Database):
	def connect(self, path):
		super().connect(path)
		# print('hello')

EditorPrefs = Preference()
