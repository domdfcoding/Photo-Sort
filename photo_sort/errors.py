#!/usr/bin/env python3
#
#  errors.py
#
#  Copyright © 2014-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from typing import Optional

__all__ = ["ExifError"]


class ExifError:
	"""
	Class for showing error messages on various exif-related errors.

	:param message: Custom message
	"""

	def __init__(self, message: Optional[str] = None):
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

		self.message = "Unable to parse EXIF data."
		return self

	def open_error(self):
		"""
		Error when a file cannot be opened.
		"""

		self.message = "Cannot open for reading."
		return self

	def no_data(self):
		"""
		Error when no EXIF data is found.
		"""

		self.message = "No EXIF data found"
		return self

	def copy_error(self):
		"""
		Error when the file cannot be copied.
		"""

		self.message = "Could not copy file."
		return self

	def move_error(self):
		"""
		Error when the file cannot be moved.
		"""

		self.message = "Could not move file."
		return self
