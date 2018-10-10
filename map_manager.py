import numpy
from PIL import Image

# filename is a .png file containing an initial occupancy grid represented in black and white
class MapManager:
	def __init__(self, filename):
		img = Image.open(filename)
		self.occupancy_grid = numpy.array(img, dtype=bool)
		self.shape = self.occupancy_grid.shape

	def add_object(self, coords, radius):
		b, a = coords
		nx, ny = self.shape
		y, x = numpy.ogrid[-a:nx-a, -b:ny-b]
		mask = x*x + y*y <= radius*radius
		self.occupancy_grid[mask] = True

	def is_occupied(self, coords):
		return self.occupancy_grid[coords[1], coords[0]]