#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.3 on Sun Jul 14 22:10:15 2019
#

# This is an automatically generated file.
# Manual changes will be overwritten without warning!

import wx
from Launcher import Launcher


class photo_sort(wx.App):
	def OnInit(self):
		self.photo_sort = Launcher(None, wx.ID_ANY, "")
		self.SetTopWindow(self.photo_sort)
		self.photo_sort.Show()
		return True

# end of class photo_sort

if __name__ == "__main__":
	photo_sort = photo_sort(0)
	photo_sort.MainLoop()
