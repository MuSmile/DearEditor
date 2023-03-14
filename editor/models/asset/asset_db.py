from editor.common.database import Database


class _AssetDatabase(Database):
	def connect(self, path):
		super().connect(path)
		self.setupFileWatcher()
		# print('hello')

	def setupFileWatcher():
		pass

	def importAsset():
		pass

	def importAllAssets():
		pass

AssetDatabase = _AssetDatabase()
