# class to start up the game, manage the window, and translate clicks into game coordinates

import pyautogui
import subprocess
import time
import pytesseract

import game_constants
import towers

def get_numbers(string_with_numbers):
	# only get the characters that are numbers
	new_string = ''.join(ch for ch in string_with_numbers if ch.isdigit())
	return int(new_string)

def get_average_color(im):
    # Returns a 3-tuple containing the RGB value of the average color of the image
 
    r, g, b = 0, 0, 0
    count = 0
    width, height = im.size
    for s in range(width):
        for t in range(height):
            pixlr, pixlg, pixlb = im.getpixel((s, t))
            r += pixlr
            g += pixlg
            b += pixlb
            count += 1
    return ((r/count), (g/count), (b/count))

class game_manager:
	def __init__(self):
		self.anchor_x = None
		self.anchor_y = None
		self.window_width = None
		self.window_height = None

	def relative_coords_to_absolute(self, relative_coords):
		# translates from coordinates relative to the window anchor to screen coordinates 
		if self.anchor_x is None or self.anchor_y is None:
			print("window dimensions not yet initialized")
			return
		if self.window_width is None or self.window_height is None:
			print("window dimensions not yet initialized")
			return
		(relative_x, relative_y) = relative_coords
		if relative_x < 0 or relative_y < 0:
			print("out of bounds")
		if relative_x > self.window_width or relative_y > self.window_height:
			print("out of bounds")

		relative_x = min(max(0, relative_x), self.window_width)
		relative_y = min(max(0, relative_y), self.window_height)
		abs_x = relative_x + self.anchor_x
		abs_y = relative_y + self.anchor_y

		return (abs_x, abs_y)	

	def click(self, relative_coords):
		(abs_x, abs_y) = self.relative_coords_to_absolute(relative_coords)
		pyautogui.click(x=abs_x, y=abs_y)

	def click_start_round(self):
		self.click(game_constants.start_button_coords)

	def start(self):
		self.game_process = subprocess.Popen(["./flashplayer","bloonstd_moved.swf"])

		# use xwininfo to get the window dimensions and locations
		# wait for window to spawn
		time.sleep(0.5)
		xwininfo_call_args = ["xwininfo","-name","Adobe Flash Player 31,0,0,108"]
		xwininfo_response = subprocess.check_output(xwininfo_call_args)
		xwininfo_response_lines = str(xwininfo_response).split("\\n")
		for line in xwininfo_response_lines:
			if "Absolute upper-left X" in line:
				self.anchor_x = get_numbers(line)
			if "Absolute upper-left Y" in line:
				self.anchor_y = get_numbers(line)
			if "Width" in line:
				self.window_width = get_numbers(line)
			if ("Height") in line:
				self.window_height = get_numbers(line)

		# todo: consider putting this in a callback
		time.sleep(game_constants.startup_time)
		self.click(game_constants.new_game_button_coords)

	def print_relative_mouse_position(self):
		abs_p = pyautogui.position()
		print(abs_p[0] - self.anchor_x, abs_p[1] - self.anchor_y)

	def get_stats(self):
		# get the stats by taking a screenshot and then doing OCR with tesseract
		bounding_box = (self.anchor_x + game_constants.stats_box_x,
			self.anchor_y + game_constants.stats_box_y,
			game_constants.stats_box_width,
			game_constants.stats_box_height)
		im = pyautogui.screenshot(region=bounding_box)
		text = pytesseract.image_to_string(im)
		print(text)
		lines = text.split("\n")

		# make sure we got all the stats and that tesseract didn't mess up
		# also, tesseract is bad at differentiating between Os and 0s, so help it out
		if "Round" not in lines[0]:
			print("problem finding round")
		round_number = get_numbers(lines[0].replace("O","0"))
		if "Money" not in lines[1]:
			print("problem finding money")
		money = get_numbers(lines[1].replace("O","0"))
		if "Lives" not in lines[2]:
			print("problem finding lives")
		lives = get_numbers(lines[2].replace("O","0"))
		return (round_number, money, lives)

	def click_tower_button(self, tower_type):
		if tower_type == towers.tower_types.DART:
			self.click(game_constants.dart_tower_button_coords)
		if tower_type == towers.tower_types.TACK:
			self.click(game_constants.tack_tower_button_coords)
		if tower_type == towers.tower_types.ICE:
			self.click(game_constants.ice_tower_button_coords)
		if tower_type == towers.tower_types.BOMB:
			self.click(game_constants.bomb_tower_button_coords)
		if tower_type == towers.tower_types.SUPER:
			self.click(game_constants.super_tower_button_coords)

	def build_tower(self, tower_type, coords):
		self.click_tower_button(tower_type)
		# the caller of this function must determine if the location is feasible
		# otherwise it will not actually be built
		self.click(coords)
		# todo: call ESC keypress in case the tower was not actually built

	# use a screenshot to visually determine if a tower can be built somewhere
	def is_feasible_test(self, coords):
		self.click_tower_button(towers.tower_types.DART)
		(abs_x, abs_y) = self.relative_coords_to_absolute(coords)
		pyautogui.moveTo(abs_x, abs_y)
		bounding_box = (self.anchor_x,
			self.anchor_y,
			self.window_width,
			self.window_height)
		im = pyautogui.screenshot(region=bounding_box)
		(r, g, b) = get_average_color(im)
		print(b)
		return b > 79

	def end(self):
		self.game_process.terminate()
		self.anchor_x = None
		self.anchor_y = None
		self.window_width = None
		self.window_height = None
