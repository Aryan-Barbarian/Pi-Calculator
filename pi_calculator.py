import random
import math
import Geometry

def pi_rand_generator():
	#This generates PI values using the point method explained in the README
	total_points = 0
	points_in_circle = 0
	in_circle = False

	while  True:
		in_circle = False
		total_points += 1
		x = random.random()
		y = random.random()
		if (math.sqrt(x*x + y*y) <= 1):
			points_in_circle += 1
			in_circle = True
		ans = Geometry.Point(x,y)
		
		"""this yields a pair of values, the new calculation of pi
		and the actual point that was placed on the screen"""
		yield 4*(points_in_circle*1.0 / total_points),ans,in_circle

def pi_polygon_generator(radius):
	#This generates PI values using the polygon method explained in the README
	def find_point_to_add(p1,p2):
		m = -1.0 / p1.slope(p2)
		
		C = p1.midpoint(p2)

		#cons just represents all the constants. This just makes calculations easier
		cons = -C.x*m + C.y

		#the math behind these equations is explained in the README video
		x = math.sqrt((radius*radius-cons*cons*1.0) / (m*m + 1))
		y = math.sqrt(radius*radius - x*x)

		ans = Geometry.Point(x,y)
		return ans

	shape = Geometry.Polygon((Geometry.Point(0,0) , \
		Geometry.Point(radius,0), Geometry.Point(0,radius)))
	yield shape #the first shape, a triangle


	while True:
		i = 1
		max_i = len(shape.points) -1
		"""this iterates through all the existing points.
		Each time it yields, it adds a point between the point
		it is currently on and the next point and yields the 
		current shape, a Polygon object"""
		while i<max_i:
			first,second = shape.points[i:i+2]
			point_to_add = find_point_to_add(first,second)
			shape = shape.add_point(point_to_add,False)
			yield shape

			#this allows us to jump to the next two original points
			i += 2
			max_i += 1