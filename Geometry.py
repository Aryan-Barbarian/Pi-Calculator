import pygame, sys
from pygame.locals import *
import math

class Point():
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def __repr__(self):
		return "Point("+str(self.x) + ", " + str(self.y) + ")"

	
	def to_tuple(self):
		return (self.x,self.y)

	def distance_to(self,p):
		dx = self.x - p.x
		dy = self.y - p.y
		d2 = dx*dx + dy*dy
		return math.sqrt(d2)

	def area_under(self,p1):
		"""returns the area under the line between this and p1,
		another point."""
		dx = self.x - p1.x
		y = (self.y+p1.y)/2.0
		return dx*y

	def slope(self,p1):
		return (self.y - p1.y*1.0) / (self.x - p1.x)

	def midpoint(self,p1):
		x = (self.x + p1.x)/2.0
		y = (self.y + p1.y)/2.0
		return Point(x,y)

class Polygon():
	def __init__(self,points,calc_points=True):
		#set calc_points to true to calculate centroid and area at the begining
		self.points = points
		if calc_points:
			self.centroid = self.gen_centroid()
			self.area = self.gen_area()

	def gen_centroid(self):
		x = sum([p.x for p in self.points])/len(self.points)
		y = sum([p.y for p in self.points])/len(self.points)

		return Point(x,y)

	def gen_area(self):
		points = self.points + (self.points[0],)
		#print("points",points)
		ans = 0
		for i in range(len(points)-1):
			
			first,second = points[i:i+2]

			ans += first.area_under(second)
		return ans

	def add_point(self, p1,calc_points):
		"""adds a new point to the polygon. It connects the point to
		the two points on the polygon closest to it

		This is still in progress, as there are some shapes for which 
		this method doesn't work. However, this always works for regular 
		concave shapes, so it will work for the Pi Calculator
		"""
		close_first, close_second = self.closest_two_points(p1)
		points = self.points + (self.points[0],)
		for i in range(len(self.points)):
			first,second = points[i:i+2]
			if (first == close_first and second == close_second):
				arg = points[0:i] + (first,p1,second) + self.points[i+2:]
				return Polygon(arg,calc_points)
			i += 1

	def closest_two_points(self,p1):
		#returns two points on this polygon that are the closest to p1
		cP1,cP2 = self.points[0:2] #will be the current points being considered
		aP1,aP2 = self.points[0:2] #these represent the closest points so far
		points = self.points
		points = points + (points[0],) #this allows points to be considered as a
										#polygon where all points are connected,
										#linking the last and first points
		aDistance = p1.distance_to(aP1) + p1.distance_to(aP2) #this is the closest distance so far seen
		for i in range(len(self.points)-1):
			cP1,cP2 = points[i], points[i+1]
			
			cDistance = p1.distance_to(cP1) + p1.distance_to(cP2)
			if cDistance < aDistance:
				aDistance = cDistance
				aP1,aP2 = cP1,cP2
			i += 1

		return aP1,aP2

	def imperative(self,p1,p2,true_point):
		"""an imperative is similar to an inequality.
		It creates an imaginary line between p1 and p2.
		It also takes a third point, called true point,
		which represents a point that if fed to this function
		must return true.

		If true point is above the p1-p2 line, then this 
		function will return another function, check, where any
		point above the line will return true. The reverse is true
		if true point is below the p1-p2 line.
		"""
		x1 = p1.x
		y1 = p1.y

		x2 = p2.x
		y2 = p2.y

		if x1 - x2 == 0:
			if true_point.x >= x1:
				return lambda p: p.x > x1
			if true_point.x < x1:
				return lambda p: p.x < x1

		m = (y2 - y1) / (x2 - x1)
		if (true_point.y >= m*(true_point.x-x1)+y1):
			check = lambda p: p.y >= m*(p.x-x1)+y1
		if (true_point.y < m*(true_point.x-x1)+y1):
			check = lambda p: p.y < m*(p.x-x1)+y1
		return check
	
	def contains(self,p1):
		"""basically creates a list of imperatives from
		all the points of the polygon and assumes that the centroid
		is inside the polygon and uses it as the true_point for
		every imperative. This essentially checks to see that p1 is 
		inside the polygon by making sure that p1 is on the same side
		of each side of the polygon as the centroid"""
		centroid = self.centroid

		imperatives = []

		for i in range(len(self.points)-1):
			imperatives.append(self.imperative(self.points[i],self.points[i+1],centroid))

		imperatives.append(self.imperative(self.points[len(self.points)-1],self.points[0],centroid))

		for imp in imperatives:
			if imp(p1) is False:
				return False
		return True

	def to_tuple(self):
		lst = [p.to_tuple() for p in self.points]
		return tuple(lst)

	def __repr__(self):
		ans = "Polygon(" + self.points[0].__repr__()
		for el in self.points[1:]:
			ans += ", " + el.__repr__()
		return ans + ")"