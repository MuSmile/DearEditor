from editor.common.database import Database

class AssetDatabase(Database):
	def connect(self, path):
		super().connect(path)
		self.setupFileWatcher()
		# print('hello')

	def setupFileWatcher(self):
		pass

	def refresh(self):
		"""Import any changed assets.
		"""
		pass

	def importAsset(self, path):
		"""Import asset at path.
		
		Args:
			str path: Project relative path of the asset or folder to import.
		"""
		pass
	def reimportAll():
		pass

	def openAsset(self, path, lineNumber, columnNumber):
		"""Opens the asset with associated application.
		
		Args:
			str path: Project relative path of the asset or folder to open.
			int lineNumber: Line number to open with.
			int columnNumber: Column number to open with.
		"""
		pass
	def findAssets(self, filter, searchInFolders = None):
		"""Search the asset database using the search filter string.
		
		Args:
			str filter: The filter string can contain search data. See below for details about this string.
			list[str] searchInFolders: The folders where the search will start..

		Returns:
			list[str]: Array of matching asset. Note that GUIDs will be returned. If no matching assets were found, returns empty array.
		"""
		pass

	def copyAsset(self, path, newPath):
		"""Duplicates the asset at path and stores it at newPath.
		
		Args:
			str path: Filesystem path of the source asset.
			str newPath: Filesystem path of the new asset to create.

		Returns:
			boolean: Returns ``True`` if the copy operation is successful or ``False`` if part of the process fails.
		"""
		pass
	def renameAsset(self, pathName, newName):
		"""Rename an asset file.
		
		Args:
			str pathName: The path where the asset currently resides.
			str newName: The new name which should be given to the asset.

		Returns:
			str: An empty string if the asset can be moved, otherwise an error message.
		"""
		pass
	def validateMoveAsset(self, oldPath, newPath):
		"""Checks if an asset file can be moved from one folder to another. (Without actually moving the file).
		
		Args:
			str oldPath: The path where the asset currently resides.
			str newPath: The path which the asset should be moved to.

		Returns:
			str: An empty string if the asset can be moved, otherwise an error message.
		"""
		pass
	def moveAsset(self, oldPath, newPath):
		"""Move an asset file (or folder) from one folder to another.
		
		Args:
			str oldPath: The path where the asset currently resides.
			str newPath: The path which the asset should be moved to.

		Returns:
			str: An empty string if the asset can be moved, otherwise an error message.
		"""
		pass
	def moveAssetToTrash(self, path):
		"""Moves the specified asset or folder to the OS trash.
		
		Args:
			str path: Project relative path of the asset or folder to be deleted.

		Returns:
			boolean: Returns ``True`` if the asset has been successfully removed, ``False`` if it doesn't exist or couldn't be removed.
		"""
		pass
	def moveAssetsToTrash(self, paths):
		"""Moves the specified asset or folder to the OS trash.
		
		Args:
			list[str] paths: Project relative paths of the asset or folder to be deleted.

		Returns:
			list[str]: Failed paths.
		"""
		pass
	def deleteAsset(self, path):
		"""Deletes the specified asset or folder.
		
		Args:
			str path: Project relative path of the asset or folder to be deleted.

		Returns:
			boolean: Returns ``True`` if the asset has been successfully removed, ``False`` if it doesn't exist or couldn't be removed.
		"""
		pass
	def deleteAssets(self, paths):
		"""Deletes the specified assets or folders.
		
		Args:
			list[str] paths: Project relative paths of the asset or folder to be deleted.

		Returns:
			list[str]: Failed paths.
		"""
		pass

	def assetPathToGuid(self, path):
		"""Get the GUID for the asset at path.
		
		Args:
			str path: Filesystem path for the asset.

		Returns:
			str: GUID.
		"""
		pass
	def guidToAssetPath(self, guid):
		"""Gets the corresponding asset path for the supplied GUID, or an empty string if the GUID can't be found.
		
		Args:
			str guid: The GUID of an asset.

		Returns:
			str: Path of the asset relative to the project folder.
		"""
		pass

	def generateUniqueAssetPath(self, path):
		"""Creates a new unique path for an asset.
		
		Args:
			str path: Filesystem path for the asset.

		Returns:
			str: Unique for the asset.
		"""
		pass
	def getMainAssetTypeAtPath(self, path):
		"""Returns the type of the main asset object at assetPath.
		
		Args:
			str path: Filesystem path of the asset to load.

		Returns:
			str: Main asset type of the asset.
		"""
		pass
	def getTypeFromPathAndFileID(self, assetPath, localIdentifierInFile):
		"""Gets an object's type from an Asset path and a local file identifier.
		
		Args:
			str assetPath: The Asset's path.
			str localIdentifierInFile: The object's local file identifier.

		Returns:
			str: The object's type.
		"""
		pass
	def getAllAssetPaths(self):
		pass
	def contains(self, guid):
		pass

	def getMetaFilePathFromAssetPath(self, path):
		"""Gets the path to the text .meta file associated with an asset.
		
		Args:
			str path: The path to the asset.

		Returns:
			str: The path to the .meta text file or an empty string if the file does not exist.
		"""
		pass
	def getSubFolders(self, path):
		"""Given a path to a directory in the Assets folder, relative to the project folder, this method will return an array of all its subdirectories.
		
		Args:
			str path: Project relative path of the folder.

		Returns:
			list[str]: Sub folders for the given folder.
		"""
		pass

	def setLabels(self, path, labels):
		"""Replaces that list of labels on an asset.
		
		Args:
			str path: Asset path.
			list[str] labels: Asset labels.
		"""
		pass
	def getLabels(self, path):
		"""Returns all labels attached to a given asset.
		
		Args:
			str path: Asset path.

		Returns:
			list[str]: Asset labels.
		"""
		pass
	def clearLabels(self, path):
		"""Removes all labels attached to an asset.
		
		Args:
			str path: Asset path.
		"""
		pass

	def getAvailableImporterTypes(self, path):
		"""Gets the importer types associated with a given Asset type.
		
		Args:
			str path: The Asset path.

		Returns:
			list[str]: Returns an array of importer types that can handle the specified Asset.
		"""
		pass
	def setImporterOverride(self, path, importer):
		"""Set override importer for the asset.
		
		Args:
			str path: Asset path.
			AssetImporter importer: Asset importer.
		"""
		pass
	def getImporterOverride(self, path):
		"""Returns the type of the override importer.
		
		Args:
			str path: Asset path.

		Returns:
			str: Importer type.
		"""
		pass
	def clearImporterOverride(self, path):
		"""Clears the importer override for the asset.
		
		Args:
			str path: Asset path.
		"""
		pass


assetDB = AssetDatabase()
