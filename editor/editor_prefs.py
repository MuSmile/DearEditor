from editor.common.database import Database


class _Preference(Database):
	def connect(self, path):
		super().connect(path)
		# print('hello')


EditorPrefs = _Preference()
