#!/usr/bin/env python
#
# generated by wxGlade 0.9.3 on Sun Jul 14 22:10:15 2019
#

# This is an automatically generated file.
# Manual changes will be overwritten without warning!

# 3rd party
import wx  # type: ignore  # nodep

# this package
from photo_sort.launcher import Launcher

__all__ = ["photo_sort"]


class PhotoSort(wx.App):

	def OnInit(self):
		self.photo_sort = Launcher(None, wx.ID_ANY, '')
		self.SetTopWindow(self.photo_sort)
		self.photo_sort.Show()
		return True


# end of class photo_sort

if __name__ == "__main__":
	photo_sort = PhotoSort(0)
	photo_sort.MainLoop()
