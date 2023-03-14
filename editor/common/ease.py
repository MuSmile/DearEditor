"""This module provide common ease functions.
"""

from math import cos, sin, pow, sqrt
from math import pi as PI

def easeInSine(x):
	return 1 - cos((x * PI) / 2)
def easeOutSine(x):
	return sin((x * PI) / 2)
def easeInOutSine(x):
	return -(cos(PI * x) - 1) / 2

def easeInQuad(x):
	return x * x
def easeOutQuad(x):
	return 1 - (1 - x) * (1 - x)
def easeInOutQuad(x):
	if x < 0.5: return 2 * x * x
	else: return 1 - pow(-2 * x + 2, 2) / 2

def easeInCubic(x):
	return x * x * x
def easeOutCubic(x):
	return 1 - pow(1 - x, 3)
def easeInOutCubic(x):
	if x < 0.5: return 4 * x * x * x
	else: return 1 - pow(-2 * x + 2, 3) / 2

def easeInQuart(x):
	return x * x * x * x
def easeOutQuart(x):
	return 1 - pow(1 - x, 4)
def easeInOutQuart(x):
	if x < 0.5: return 8 * x * x * x * x
	else: return 1 - pow(-2 * x + 2, 4) / 2

def easeInQuint(x):
	return x * x * x * x * x
def easeOutQuint(x):
	return 1 - pow(1 - x, 5)
def easeInOutQuint(x):
	if x < 0.5: return 16 * x * x * x * x * x
	else: return 1 - pow(-2 * x + 2, 5) / 2


def easeInExpo(x):
	if x == 0: return 0
	else: return pow(2, 10 * x - 10)
def easeOutExpo(x):
	if x == 1: return 1
	else: return 1 - pow(2, -10 * x)
def easeInOutExpo(x):
	if x == 0: return 0
	if x == 1: return 1
	if x < 0.5: return pow(2, 20 * x - 10) / 2
	else: return (2 - pow(2, -20 * x + 10)) / 2


def easeInCirc(x):
	return 1 - sqrt(1 - pow(x, 2))
def easeOutCirc(x):
	return sqrt(1 - pow(x - 1, 2))
def easeInOutCirc(x):
	if x < 0.5: return (1 - sqrt(1 - pow(2 * x, 2))) / 2
	else: return (sqrt(1 - pow(-2 * x + 2, 2)) + 1) / 2

def easeInBack(x):
	c1 = 1.70158
	c3 = c1 + 1
	return c3 * x * x * x - c1 * x * x
def easeOutBack(x):
	c1 = 1.70158
	c3 = c1 + 1
	return 1 + c3 * pow(x - 1, 3) + c1 * pow(x - 1, 2)
def easeInOutBack(x):
	c1 = 1.70158
	c2 = c1 * 1.525
	if x < 0.5: return (pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2
	else: return (pow(2 * x - 2, 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2


def easeInElastic(x):
	if x == 0: return 0
	if x == 1: return 1
	c4 = (2 * PI) / 3
	return -pow(2, 10 * x - 10) * sin((x * 10 - 10.75) * c4)
def easeOutElastic(x):
	if x == 0: return 0
	if x == 1: return 1
	c4 = (2 * PI) / 3
	return pow(2, -10 * x) * sin((x * 10 - 0.75) * c4) + 1
def easeInOutElastic(x):
	if x == 0: return 0
	if x == 1: return 1
	c5 = (2 * PI) / 4.5
	if x < 0.5: return -(pow(2, 20 * x - 10) * sin((20 * x - 11.125) * c5)) / 2
	else: return (pow(2, -20 * x + 10) * sin((20 * x - 11.125) * c5)) / 2 + 1

def easeInBounce(x):
	return 1 - easeOutBounce(1 - x)
def easeOutBounce(x):
	n1 = 7.5625
	d1 = 2.75
	if x < 1 / d1:
		return n1 * x * x
	elif x < 2 / d1:
		x = x - 1.5
		return n1 * (x / d1) * x + 0.75
	elif x < 2.5 / d1:
		x = x - 2.25
		return n1 * (x / d1) * x + 0.9375
	else:
		x = x - 2.625
		return n1 * (x / d1) * x + 0.984375
def easeInOutBounce(x):
	if x < 0.5: return (1 - easeOutBounce(1 - 2 * x)) / 2
	else: return (1 + easeOutBounce(2 * x - 1)) / 2


if __name__ == '__main__':
	print(easeInSine(0.5))
	print(easeOutSine(0.5))
	print(easeInOutSine(0.5))
	
	print(easeInQuad(0.5))
	print(easeOutQuad(0.5))
	print(easeInOutQuad(0.5))
	
	print(easeInCubic(0.5))
	print(easeOutCubic(0.5))
	print(easeInOutCubic(0.5))
	
	print(easeInQuart(0.5))
	print(easeOutQuart(0.5))
	print(easeInOutQuart(0.5))
	
	print(easeInQuint(0.5))
	print(easeOutQuint(0.5))
	print(easeInOutQuint(0.5))
	
	print(easeInExpo(0.5))
	print(easeOutExpo(0.5))
	print(easeInOutExpo(0.5))

	print(easeInCirc(0.5))
	print(easeOutCirc(0.5))
	print(easeInOutCirc(0.5))

	print(easeInBack(0.5))
	print(easeOutBack(0.5))
	print(easeInOutBack(0.5))

	print(easeInElastic(0.5))
	print(easeOutElastic(0.5))
	print(easeInOutElastic(0.5))

	print(easeInBounce(0.5))
	print(easeOutBounce(0.5))
	print(easeInOutBounce(0.6))
