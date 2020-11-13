# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.3 on Sun Jul 14 22:06:48 2019
#

import wx
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class SettingsDialog(wx.Dialog):
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
