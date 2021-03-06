#!/usr/bin/env python3
#
#  manage_cameras.py
"""
Provides a class to manage the mapping of camera IDs to human-readable names.
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

# stdlib
import json
from typing import Dict

# 3rd party
import exifread  # type: ignore
import exiftool  # type: ignore
import wx  # type: ignore  # nodep
import wx.grid  # type: ignore  # nodep

__all__ = ["manage_cameras"]

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class ManageCameras(wx.Dialog):
	"""
	Class to manage the mapping of camera IDs to human-readable names.

	:param parent:
	:param id:
	:param title:
	:param pos:
	:param size:
	:param style:
	:param name:
	:param data:
	"""

	# TODO: docstring for __init__'s arguments

	def __init__(
			self,
			parent,
			id=wx.ID_ANY,  # noqa: A002  # pylint: disable=redefined-builtin
			title='',
			pos=wx.DefaultPosition,
			size=wx.DefaultSize,
			style=wx.DEFAULT_DIALOG_STYLE,
			name=wx.DialogNameStr,
			data=None
			):

		if not data:
			data = {}

		args = (parent, id)
		kwds = {
				"title": title,
				"pos": pos,
				"size": size,
				"style": style,
				"name": name,
				}

		# begin wxGlade: manage_cameras.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
		wx.Dialog.__init__(self, *args, **kwds)
		self.SetSize((400, 328))
		self.add_btn = wx.Button(self, wx.ID_ADD, '')
		self.add_from_btn = wx.Button(self, wx.ID_ANY, "Add from Image")
		self.remove_btn = wx.Button(self, wx.ID_REMOVE, '')
		self.grid_1 = wx.grid.Grid(self, wx.ID_ANY, size=(1, 1))
		self.cancel_btn = wx.Button(self, wx.ID_CANCEL, '')
		self.apply_btn = wx.Button(self, wx.ID_APPLY, '')

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self.do_add, self.add_btn)
		self.Bind(wx.EVT_BUTTON, self.do_add_from, self.add_from_btn)
		self.Bind(wx.EVT_BUTTON, self.do_remove, self.remove_btn)
		self.Bind(wx.EVT_BUTTON, self.do_apply, self.apply_btn)
		# end wxGlade
		self.grid_1.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.on_select_cell)
		self.grid_1.DeleteRows(1, 10)

		row = 0

		for camera in data:
			self.grid_1.SetCellValue(row, 0, camera)
			self.grid_1.SetCellValue(row, 1, data[camera])
			row += 1
			self.grid_1.AppendRows()

		self.cur_row = 0
		self.cur_col = 0

		self.grid_1.GoToCell(0, 0)
		self.grid_1.SetFocus()

	def __set_properties(self) -> None:
		# begin wxGlade: manage_cameras.__set_properties
		self.SetTitle("Manage Cameras")
		self.SetSize((400, 328))
		self.grid_1.CreateGrid(10, 2)
		self.grid_1.SetColLabelValue(0, "Exif Camera")
		self.grid_1.SetColSize(0, 180)
		self.grid_1.SetColLabelValue(1, "Pretty Name")
		self.grid_1.SetColSize(1, 180)
		# end wxGlade
		self.grid_1.HideRowLabels()

	def __do_layout(self) -> None:
		# begin wxGlade: manage_cameras.__do_layout
		sizer_3 = wx.BoxSizer(wx.VERTICAL)
		sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_4.Add(self.add_btn, 0, wx.ALIGN_CENTER | wx.RIGHT, 3)
		sizer_4.Add(self.add_from_btn, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 3)
		sizer_4.Add(self.remove_btn, 0, wx.ALIGN_CENTER | wx.LEFT, 3)
		sizer_3.Add(sizer_4, 0, wx.ALIGN_CENTER | wx.BOTTOM | wx.TOP, 10)
		sizer_3.Add(self.grid_1, 1, wx.EXPAND, 0)
		sizer_7.Add(self.cancel_btn, 0, wx.RIGHT, 7)
		sizer_7.Add(self.apply_btn, 0, wx.RIGHT, 7)
		sizer_3.Add(sizer_7, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
		self.SetSizer(sizer_3)
		self.Layout()
		# end wxGlade

	def do_apply(self, event) -> None:  # wxGlade: manage_cameras.<event_handler>
		if self.Validate() and self.TransferDataFromWindow():

			if self.IsModal():
				self.EndModal(wx.ID_APPLY)
			else:
				self.SetReturnCode(wx.ID_APPLY)
				self.Show(False)

		event.Skip()

	def do_add(self, event) -> None:  # wxGlade: manage_cameras.<event_handler>
		self.grid_1.AppendRows()
		event.Skip()

	def do_remove(self, event) -> None:  # wxGlade: manage_cameras.<event_handler>
		print(self.grid_1.GetSelectedCells())
		print(self.cur_row)
		if self.grid_1.GetNumberRows() == 1:
			print("You can not remove the last entry!")
			return
		self.grid_1.DeleteRows(self.cur_row)
		self.grid_1.GoToCell(self.cur_row, self.cur_col)
		self.grid_1.SetFocus()

		event.Skip()

	def on_select_cell(self, event) -> None:
		self.cur_row = event.GetRow()
		self.cur_col = event.GetCol()
		print(self.cur_col, self.cur_row)
		event.Skip()

	def get_data(self) -> Dict:
		data = {}
		for row in range(self.grid_1.GetNumberRows()):
			exif_camera = self.grid_1.GetCellValue(row, 0)
			pretty_name = self.grid_1.GetCellValue(row, 1)
			if any([pretty_name == '', exif_camera == '']):
				continue
			data[exif_camera] = pretty_name
		return data

	def do_add_from(self, event) -> None:  # wxGlade: manage_cameras.<event_handler>

		with wx.FileDialog(
				self,
				"Open Image File",  # wildcard="JPEG files (*.jpg;*.jpeg;*.JPG)|*.jpg;*.jpeg;*.JPG",
				style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
				) as fileDialog:

			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return  # the user changed their mind

			# print(style)
			# print(wx.FD_MULTIPLE in style)

			pathname = fileDialog.GetPath()

			print(pathname)

			try:
				with open(pathname, "rb") as file:
					data = exifread.process_file(file)
					exif_camera = str(data["Image Model"])

			except (OSError, KeyError):
				# wx.MessageDialog(self, f"Cannot open file '{pathname}'.", "Error",
				# 				 style=wx.OK | wx.ICON_ERROR).ShowModal()
				# Video File

				with exiftool.ExifTool() as et:
					try:
						data = et.get_metadata(pathname)
					except json.decoder.JSONDecodeError:
						wx.MessageDialog(
								self, f"Cannot open file '{pathname}'.", "Error", style=wx.OK | wx.ICON_ERROR
								).ShowModal()

					# Video files, Canon
					try:
						exif_camera = str(data["EXIF:Model"])
					except KeyError:
						# Video files, Panasonic
						try:
							exif_camera = str(data["MakerNotes:Model"])
						except KeyError:
							# Video files, GoPro 7
							try:
								exif_camera = str(data["QuickTime:Model"])
							except KeyError:
								try:
									exif_camera = str(data["QuickTime:LensSerialNumber"])
								except KeyError:
									wx.MessageDialog(
											self,
											f"Cannot parse EXIF data from file '{pathname}'.",
											"Error",
											style=wx.OK | wx.ICON_ERROR
											).ShowModal()
									event.Skip()
									return

					print(exif_camera)

					for row in range(self.grid_1.GetNumberRows()):
						if exif_camera == self.grid_1.GetCellValue(row, 0):
							wx.MessageDialog(
									self,
									f"The camera '{exif_camera}' is already in the table.",
									"Error",
									style=wx.OK | wx.ICON_ERROR
									).ShowModal()
							return
				self.grid_1.SetCellValue(self.grid_1.GetNumberRows() - 1, 0, exif_camera)
				self.grid_1.AppendRows()

		event.Skip()


# end of class manage_cameras
