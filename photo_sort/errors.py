#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  errors.py
#
#  Copyright (c) 2019.  Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#


class exif_error(object):
	"""
	Class for showing error messages on various exif-related errors
	"""
	
	def __init__(self, message=None):
		"""
		Init exif_error class

		:param message: Custom message
		:type message@ str
		"""
		
		self.message = message
	
	def show(self, filename_string):
		"""
		Show the error message

		:param filename_string: Filename that caused the error
		:type filename_string: str
		"""
		
		print(f"\r'{filename_string}': {self.message}.\n")
	
	def parse_error(self):
		"""
		Error when EXIF data cannot be parsed
		"""
		
		self.message = "Unable to parse EXIF data"
		return self
	
	def open_error(self):
		"""
		Error when file cannot be opened
		"""
		
		self.message = "Cannot open for reading"
		return self
	
	def no_data(self):
		"""
		Error when no EXIF data is found
		"""
		
		self.message = "No EXIF data found"
		return self
	
	def copy_error(self):
		"""
		Error when the file cannot be copied
		"""
		
		self.message = "Could not copy file"
		return self
	
	def move_error(self):
		"""
		Error when the file cannot be moved
		"""
		
		self.message = "Could not move file"
		return self

