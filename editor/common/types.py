"""This module provides basic types.
"""

from PySide6.QtGui import QColor

###############  VECTOR2 ###############
class Vector2:
	"""Represent a vector2 data.

	Provide a group of class members for quick usage:

	.. code-block:: python
	   :linenos:

	   assert(Vector2.zero  == Vector2( 0,  0))
	   assert(Vector2.left  == Vector2(-1,  0))
	   assert(Vector2.right == Vector2( 1,  0))
	   assert(Vector2.up    == Vector2( 0,  1))
	   assert(Vector2.down  == Vector2( 0, -1))
	   assert(Vector2.one   == Vector2( 1,  1))
	"""

	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

	def __add__(self, other):
		x = self.x + other.x
		y = self.y + other.y
		return Vector2(x, y)
	def __sub__(self, other):
		x = self.x - other.x
		y = self.y - other.y
		return Vector2(x, y)
	def __mul__(self, other):
		x = self.x * other.x
		y = self.y * other.y
		return Vector2(x, y)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	def __ne__(self, other):
		return self.x != other.x or self.y != other.y

	def __str__(self):
		return f'Vector2({self.x}, {self.y})'

	def toVec3(self):
		"""Convert to Vector3 object.

		Returns:
			Vector3: Converted Vector3 object.
		"""
		return Vector3(self.x, self.y)
	def toVec4(self):
		"""Convert to Vector4 object.

		Returns:
			Vector4: Converted Vector4 object.
		"""
		return Vector4(self.x, self.y)

Vector2.zero  = Vector2( 0,  0)
Vector2.left  = Vector2(-1,  0)
Vector2.right = Vector2( 1,  0)
Vector2.up    = Vector2( 0,  1)
Vector2.down  = Vector2( 0, -1)
Vector2.one   = Vector2( 1,  1)


###############  VECTOR3 ###############
class Vector3:
	"""Represent a vector3 data.

	Provide a group of class members for quick usage:

	.. code-block:: python
	   :linenos:

	   assert(Vector3.zero  == Vector3( 0,  0,  0))
	   assert(Vector3.left  == Vector3(-1,  0,  0))
	   assert(Vector3.right == Vector3( 1,  0,  0))
	   assert(Vector3.up    == Vector3( 0,  1,  0))
	   assert(Vector3.down  == Vector3( 0, -1,  0))
	   assert(Vector3.front == Vector3( 0,  0,  1))
	   assert(Vector3.back  == Vector3( 0,  0, -1))
	   assert(Vector3.one   == Vector3( 1,  1,  1))
	"""

	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self, other):
		x = self.x + other.x
		y = self.y + other.y
		z = self.z + other.z
		return Vector3(x, y, z)
	def __sub__(self, other):
		x = self.x - other.x
		y = self.y - other.y
		z = self.z - other.z
		return Vector3(x, y, z)
	def __mul__(self, other):
		x = self.x * other.x
		y = self.y * other.y
		z = self.z * other.z
		return Vector3(x, y, z)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.z == other.z
	def __ne__(self, other):
		return self.x != other.x or self.y != other.y or self.z != other.z

	def __str__(self):
		return f'Vector3({self.x}, {self.y}, {self.z})'

	def toVec2(self):
		"""Convert to Vector2 object.

		Returns:
			Vector2: Converted Vector2 object.
		"""
		return Vector2(self.x, self.y)
	def toVec4(self):
		"""Convert to Vector4 object.

		Returns:
			Vector4: Converted Vector4 object.
		"""
		return Vector4(self.x, self.y, self.z)

Vector3.zero  = Vector3( 0,  0,  0)
Vector3.left  = Vector3(-1,  0,  0)
Vector3.right = Vector3( 1,  0,  0)
Vector3.up    = Vector3( 0,  1,  0)
Vector3.down  = Vector3( 0, -1,  0)
Vector3.front = Vector3( 0,  0,  1)
Vector3.back  = Vector3( 0,  0, -1)
Vector3.one   = Vector3( 1,  1,  1)


###############  VECTOR4 ###############
class Vector4:
	"""Represent a vector4 data.

	Provide a group of class members for quick usage:

	.. code-block:: python
	   :linenos:

	   assert(Vector4.zero == Vector4(0, 0, 0, 0))
	   assert(Vector4.one  == Vector4(1, 1, 1, 1))
	"""

	def __init__(self, x = 0, y = 0, z = 0, w = 0):
		self.x = x
		self.y = y
		self.z = z
		self.w = w

	def __add__(self, other):
		x = self.x + other.x
		y = self.y + other.y
		z = self.z + other.z
		w = self.w + other.w
		return Vector4(x, y, z, w)
	def __sub__(self, other):
		x = self.x - other.x
		y = self.y - other.y
		z = self.z - other.z
		w = self.w - other.w
		return Vector4(x, y, z, w)
	def __mul__(self, other):
		x = self.x * other.x
		y = self.y * other.y
		z = self.z * other.z
		w = self.w * other.w
		return Vector4(x, y, z, w)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w
	def __ne__(self, other):
		return self.x != other.x or self.y != other.y or self.z != other.z or self.w != other.w

	def __str__(self):
		return f'Vector4({self.x}, {self.y}, {self.z}, {self.w})'

	def toVec2(self):
		"""Convert to Vector2 object.

		Returns:
			Vector2: Converted Vector2 object.
		"""
		return Vector2(self.x, self.y)
	def toVec3(self):
		"""Convert to Vector3 object.

		Returns:
			Vector3: Converted Vector3 object.
		"""
		return Vector3(self.x, self.y, self.z)

Vector4.zero = Vector4(0, 0, 0, 0)
Vector4.one  = Vector4(1, 1, 1, 1)


###############  COLOR ###############
class Color(QColor):
	"""Represent a color data.

	Provide a group of class members for quick usage:

	.. code-block:: python
	   :linenos:

	   assert(Color.red         == Color(255,   0,   0, 255))
	   assert(Color.green       == Color(  0, 255,   0, 255))
	   assert(Color.blue        == Color(  0,   0, 255, 255))
	   assert(Color.white       == Color(255, 255, 255, 255))
	   assert(Color.black       == Color(  0,   0,   0, 255))
	   assert(Color.transparent == Color(  0,   0,   0,   0))
	"""

	@staticmethod
	def fromString(name):
		"""Returns a Color parsed from name.

		Returns:
			Color: Parsed Color object.
		"""
		clr = QColor(name)
		return Color(clr.red(), clr.green(), clr.blue(), clr.alpha())

	@property
	def r(self):
		"""int: Color red channel, support both setter and getter.
		"""
		return super().red()
	@r.setter
	def r(self, value): self.setRed(value)
	@property
	def g(self):
		"""int: Color green channel, support both setter and getter.
		"""
		return super().green()
	@g.setter
	def g(self, value): self.setGreen(value)
	@property
	def b(self):
		"""int: Color blue channel, support both setter and getter.
		"""
		return super().blue()
	@b.setter
	def b(self, value): self.setBlue(value)
	@property
	def a(self):
		"""int: Color alpha channel, support both setter and getter.
		"""
		return super().alpha()
	@a.setter
	def a(self, value): self.setAlpha(value)

	def __init__(self, r, g, b, a = 255):
		super().__init__(r, g, b, a)

	def __mul__(self, other):
		r = round(self.redF()   * other.redF()   * 255)
		g = round(self.greenF() * other.greenF() * 255)
		b = round(self.blueF()  * other.blueF()  * 255)
		a = round(self.alphaF() * other.alphaF() * 255)
		return Color(r, g, b, a)

	def __eq__(self, other):
		print()
		return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a
	def __ne__(self, other):
		return self.r != other.r or self.g != other.g or self.b != other.b or self.a != other.a

	def __str__(self):
		return f'Color({self.r}, {self.g}, {self.b}, {self.a})'

	def toVec3(self):
		"""Convert to Vector3 object.

		Returns:
			Vector3: Converted Vector3 object.
		"""
		return Vector3(self.r, self.g, self.b)
	def toVec4(self):
		"""Convert to Vector4 object.

		Returns:
			Vector4: Converted Vector4 object.
		"""
		return Vector4(self.r, self.g, self.b, self.a)

Color.red         = Color(255,   0,   0, 255)
Color.green       = Color(  0, 255,   0, 255)
Color.blue        = Color(  0,   0, 255, 255)
Color.white       = Color(255, 255, 255, 255)
Color.black       = Color(  0,   0,   0, 255)
Color.transparent = Color(  0,   0,   0,   0)
