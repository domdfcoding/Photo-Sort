#!/usr/bin/env python3
#
#  SettingsDialog.py
"""
Provides a dialog for configuring settings.
"""
#
#  Copyright © 2014-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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

# 3rd party
import wx  # type: ignore  # nodep

__all__ = ["SettingsDialog"]

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class SettingsDialog(wx.Dialog):
	"""
	Dialog for configuring settings.
	"""

	# TODO: docstring for __init__'s arguments

	def __init__(self, *args, **kwds):
		# begin wxGlade: SettingsDialog.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: SettingsDialog.__set_properties
		self.SetTitle("dialog")
		# end wxGlade

	def __do_layout(self):
		self.CreateSeparatedButtonSizer(wx.ID_APPLY | wx.ID_CANCEL)
		# begin wxGlade: SettingsDialog.__do_layout
		self.Layout()
		# end wxGlade


# end of class SettingsDialog
