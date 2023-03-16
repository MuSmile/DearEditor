"""This module provides math toolkit.
"""

from math import cos, sin, atan2, degrees, radians
from random import random, uniform

def clamp(t, min, max):
	if t < min: return min
	if t > max: return max
	return t

def sign(x):
	if x > 0: return 1
	if x < 0: return -1
	return 0

def cosd(deg):
	return cos(radians(deg))
def sind(deg):
	return sin(radians(deg))

def getDir(dx, dy):
	return degrees(atan2(dy, dx))
def getDirBetween(p1, p2):
	l = p2 - p1
	return getDir(l.x(), l.y())
def vecAngle(dir, len):
	return cosd(dir) * len, sind(dir) * len

def randBoolean():
	return random() > 0.5
def randSign():
	return random() > 0.5 and 1 or -1
def noise(range):
	return uniform(-range, range)
# def randint() -- built-in

# warp a dir into (-180, 180]
def wrapDir(dir):
	dir %= 360
	if dir > 180: return dir - 360
	else: return dir
# warp a dir into [0, 360)
def wrapDir360(dir):
	return dir % 360

def dirDiff(dir1, dir2):
	diff = (dir2 - dir1) % 360
	if diff > 180: return diff - 360
	else: return diff


def locAt(begin, end, value):
	return (value - begin) / (end - begin)

def lerp(begin, end, t, ease = None):
	t = clamp(t, 0, 1)
	return t * end + (1 - t) * begin

def lerpI(begin, end, t, ease = None):
	return round(lerp(begin, end, t, ease))

def rangeMap(t, s1, e1, s2, e2):
	t = clamp((t - s1) / (e1 - s1), 0, 1)
	return t * e2 + (1 - t) * s2

def rangeMapI(t, s1, e1, s2, e2):
	return round(rangeMapI(t, s1, e1, s2, e2))
