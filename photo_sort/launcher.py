#!/usr/bin/env python3
#
#  Launcher.py
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
import json
import os
import shutil
from datetime import timedelta
from threading import Event, Thread
from typing import Dict, List

# 3rd party
import exifread  # type: ignore
import exiftool  # type: ignore
import wx  # type: ignore  # nodep
from domdf_python_tools.paths import maybe_make
from domdf_wxpython_tools.events import SimpleEvent  # type: ignore  # TODO
from domdf_wxpython_tools.picker import dir_picker  # type: ignore
from domdf_wxpython_tools.timer_thread import Timer, timer_event  # type: ignore

# this package
from photo_sort.errors import ExifError
from photo_sort.manage_cameras import ManageCameras
from photo_sort.settings_dialog import SettingsDialog

__all__ = ["Worker", "Launcher"]

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

progress_event = SimpleEvent("Progress")
sorting_done = SimpleEvent("Done")

worker_thread_running = False

mode_copy = 0
mode_move = 1

########################################################################


class Worker(Thread):
	"""
	Worker Thread for performing sorting.

	Includes code from https://gist.github.com/samarthbhargav/5a515a399f7113137331


	:param parent: Class to send event updates to
	:param filelist: List of file paths to sort
	:param destination: Base directory to sort files into
	:param mode: Whether to copy or move the files, default Copy
	:param within_dirs: Whether to sort within directories, default False
	:param by_datetime: Whether to sort by date and time, default False (i.e. just by date)
	:param by_camera: Whether to sort by camera name, default False
	"""

	def __init__(
			self,
			parent: wx.Window,
			filelist: List,
			destination: str,
			mode: int = mode_copy,
			within_dirs: bool = False,
			by_datetime: bool = False,
			by_camera: bool = False
			):
		self._stopevent = Event()
		Thread.__init__(self, name="WorkerThread")
		self._parent = parent
		global worker_thread_running
		worker_thread_running = True

		print(f"Destination: {destination}")
		if mode == mode_copy:
			print("Mode: Copy")
		elif mode == mode_move:
			print("Mode: Move")
		else:
			print("Unknown mode. Defaulting to 'Copy'")
			mode = mode_copy

		print(f"Sort Within Directories: {within_dirs}")
		print(f"Sort by Date and Time: {by_datetime}")
		print(f"Sort by Camera: {by_camera}")

		self.destination = destination
		self.mode = mode
		self.within_dirs = within_dirs
		self.by_datetime = by_datetime
		self.by_camera = by_camera
		self.filelist = filelist

	@staticmethod
	def parse_date(data: Dict) -> str:
		"""
		Determine the date the photograph was taken from its EXIF data

		:param data: EXIF data to find the date from
		"""

		print(data)
		try:
			date = str(data["EXIF DateTimeOriginal"])[:10]
			date = date.replace(':', '_').replace(' ', '_')
		except KeyError:

			try:
				print("attempt 2")
				date = str(data["Image DateTime"])[:10]
				date = date.replace(':', '_').replace(' ', '_')
			except KeyError:
				try:
					print("attempt 3 - video file")
					date = str(data["EXIF:DateTimeOriginal"])[:10]
					date = date.replace(':', '_').replace(' ', '_')
				except KeyError:
					try:
						print("attempt 4 - video file")
						date = str(data["QuickTime:MediaCreateDate"])[:10]
						date = date.replace(':', '_').replace(' ', '_')
					except KeyError:
						return ExifError().parse_error()

		return date

	def parse_camera(self, data: Dict) -> str:
		"""
		Determine the camera the photograph was taken with its EXIF data

		:param data: EXIF data to find the camera from
		"""

		camera = ''

		if self.by_camera:
			try:
				raw_camera = str(data["Image Model"])
				if raw_camera in self._parent.cameras:
					camera = self._parent.cameras[raw_camera]
				else:
					camera = raw_camera
			except KeyError:
				# Video files, Canon
				try:
					raw_camera = str(data["EXIF:Model"])
					if raw_camera in self._parent.cameras:
						camera = self._parent.cameras[raw_camera]
					else:
						camera = raw_camera
				except KeyError:
					# Video files, Panasonic
					try:
						raw_camera = str(data["MakerNotes:Model"])
						if raw_camera in self._parent.cameras:
							camera = self._parent.cameras[raw_camera]
						else:
							camera = raw_camera
					except KeyError:
						# Video files, GoPro 7
						try:
							raw_camera = str(data["QuickTime:Model"])
							if raw_camera in self._parent.cameras:
								camera = self._parent.cameras[raw_camera]
							else:
								camera = raw_camera
						except KeyError:
							try:
								raw_camera = str(data["QuickTime:LensSerialNumber"])
								if raw_camera in self._parent.cameras:
									camera = self._parent.cameras[raw_camera]
								else:
									camera = raw_camera
							except KeyError:
								pass

		return camera

	def run(self) -> None:
		"""
		Run Worker Thread
		"""

		print("Working...")

		for filepath in self.filelist:

			if self._stopevent.is_set():
				return

			error = False

			path_length = 80

			if len(filepath) > path_length:
				filename_string = "..." + filepath[-path_length:]
			else:
				filename_string = filepath + ' ' * (path_length - len(filepath))

			print(f'\r{filename_string}', end='')

			try:
				file = open(filepath, "rb")
			except BaseException:
				ExifError().open_error().show(filename_string)
				error = True
				continue

			# get the tags
			data = exifread.process_file(file, details=False, debug=False)

			with exiftool.ExifTool() as et:
				try:
					metadata = et.get_metadata(filepath)
				except json.decoder.JSONDecodeError:
					metadata = None

				# using exiftool as a backup for video files

			if not data:
				data = metadata
				if not metadata:
					error = True
					ExifError().no_data().show(filename_string)
			"""try:
				date = str(data['Image DateTime'])[:10]
				date = date.replace(':', '_').replace(' ', '_')
			except KeyError:

				try:
					print("attempt 2")
					date = str(data["EXIF DateTimeOriginal"])[:10]
					date = date.replace(':', '_').replace(' ', '_')
				except KeyError:
					print(f"\r'{filename_string}': Unable to parse EXIF data.\n")
					error = True"""

			date = self.parse_date(data)
			if isinstance(date, ExifError):
				error = True
				date.show(filename_string)

			if not error:

				camera = self.parse_camera(data)

				destination_path = os.path.join(self.destination, date, camera)
				maybe_make(destination_path, parents=True)

				#print(f"{date}  {camera} -> {destination_path}               ")

				destination_filename = os.path.split(filepath)[-1]

				# If file already exists, add a (number) to the end of the filename
				if os.path.isfile(os.path.join(destination_path, destination_filename)):
					# TODO: Use filecmp to see if files are identical

					num = 1
					while True:
						# Determine the fist available duplicate number
						base_filename, extension = os.path.splitext(destination_filename)
						if not os.path.isfile(f"{base_filename} ({num}){extension}"):
							destination_filename = f"{base_filename} ({num}){extension}"
							break
						num += 1

				print(f"{date}  {camera} -> {os.path.join(destination_path, destination_filename)}               ")

				if self.mode == mode_copy:
					try:
						shutil.copy2(filepath, os.path.join(destination_path, destination_filename))
					except BaseException:
						print(f"\r'{filename_string}': Could not copy file.\n")
						ExifError().copy_error().show(filename_string)

				elif self.mode == mode_move:
					try:
						shutil.move(filepath, os.path.join(destination_path, destination_filename))
					except BaseException:
						ExifError().move_error().show(filename_string)

			file.close()

			if not self._stopevent.is_set():
				# evt = ProgressEvent(myEVT_PROGRESS, -1)
				# wx.PostEvent(self._parent, evt)
				progress_event.trigger()

		global worker_thread_running
		worker_thread_running = False

		# evt = CompletionEvent(myEVT_DONE, -1)
		# wx.PostEvent(self._parent, evt)
		sorting_done.trigger()

	def join(self, timeout=None):
		"""
		Stop the thread and wait for it to end

		:param timeout:
		:type:
		"""

		self._stopevent.set()
		Thread.join(self, timeout)


########################################################################


class Launcher(wx.Frame):
	"""
	Main window for Photo Sort
	"""

	def __init__(self, *args, **kwds):
		# begin wxGlade: Launcher.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.SetSize((600, 528))
		self.panel_1 = wx.Panel(self, wx.ID_ANY)
		self.source_dir_picker = dir_picker(self.panel_1, wx.ID_ANY)
		self.destination_dir_picker = dir_picker(self.panel_1, wx.ID_ANY)
		self.copy_radio_btn = wx.RadioButton(self.panel_1, wx.ID_ANY, "Copy", style=wx.RB_GROUP)
		self.move_radio_btn = wx.RadioButton(self.panel_1, wx.ID_ANY, "Move")
		self.within_dirs_checkbox = wx.CheckBox(self.panel_1, wx.ID_ANY, "Sort Within Directories")
		self.datetime_checkbox = wx.CheckBox(self.panel_1, wx.ID_ANY, "Sort by Date and Time")
		self.camera_checkbox = wx.CheckBox(self.panel_1, wx.ID_ANY, "Sort by Camera")
		self.manage_cameras_btn = wx.Button(self.panel_1, wx.ID_ANY, "Manage Cameras")
		self.progress_gauge = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
		self.cancel_btn = wx.Button(self, wx.ID_ANY, "Close")
		self.sort_btn = wx.Button(self, wx.ID_ANY, "Sort")

		# Menu Bar
		self.Launcher_menubar = wx.MenuBar()
		wxglade_tmp_menu = wx.Menu()
		item = wxglade_tmp_menu.Append(wx.ID_ANY, "Settings FIle", '')
		self.Bind(wx.EVT_MENU, self.set_settings_file, id=item.GetId())
		self.Launcher_menubar.Append(wxglade_tmp_menu, "FIle")
		self.SetMenuBar(self.Launcher_menubar)
		# Menu Bar end

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_CHECKBOX, self.within_dirs_clicked, self.within_dirs_checkbox)
		self.Bind(wx.EVT_BUTTON, self.do_manage_cameras, self.manage_cameras_btn)
		self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancel_btn)
		self.Bind(wx.EVT_BUTTON, self.sort_handler, self.sort_btn)
		# end wxGlade

		# Bind Events
		progress_event.set_receiver(self)
		progress_event.Bind(self.increase_file_count)

		sorting_done.set_receiver(self)
		sorting_done.Bind(self.on_sort_done)

		self.Bind(wx.EVT_CLOSE, self.on_close)

		timer_event.set_receiver(self)
		timer_event.Bind(self.update_time_elapsed)

	def __set_properties(self):
		# begin wxGlade: Launcher.__set_properties
		self.SetTitle("Sort Photographs")
		self.source_dir_picker.SetMinSize((10000000, -1))
		self.copy_radio_btn.SetValue(1)
		self.camera_checkbox.SetValue(1)
		# end wxGlade

		# Load camera and directories settings

		try:
			with open("settings.json") as f:
				self.cameras, directories = json.load(f)
				self.source_dir_picker.SetInitialValue(directories["Source"])
				self.destination_dir_picker.SetInitialValue(directories["Destination"])
		except FileNotFoundError:
			self.source_dir_picker.SetInitialValue(os.path.abspath("To Sort"))
			self.destination_dir_picker.SetInitialValue(os.path.abspath("By Date"))

		self.source_dir_picker.ResetValue()
		self.destination_dir_picker.ResetValue()
		self.sort_btn.SetFocus()

	def __do_layout(self):
		# begin wxGlade: Launcher.__do_layout
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_2 = wx.BoxSizer(wx.VERTICAL)
		progress_text = wx.BoxSizer(wx.HORIZONTAL)
		grid_sizer_1 = wx.FlexGridSizer(2, 2, 0, 0)
		header_text = wx.StaticText(self.panel_1, wx.ID_ANY, "Sort Photographs By Date")
		header_text.SetFont(
				wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Ubuntu")
				)
		sizer_2.Add(header_text, 0, 0, 0)
		static_line_1 = wx.StaticLine(self.panel_1, wx.ID_ANY)
		sizer_2.Add(static_line_1, 0, wx.BOTTOM | wx.EXPAND | wx.TOP, 5)
		source_label = wx.StaticText(self.panel_1, wx.ID_ANY, "Source Directory: ")
		grid_sizer_1.Add(source_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.TOP, 3)
		grid_sizer_1.Add(self.source_dir_picker, 1, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.EXPAND | wx.TOP, 3)
		destination_label = wx.StaticText(self.panel_1, wx.ID_ANY, "Destination Directory: ")
		grid_sizer_1.Add(destination_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.TOP, 3)
		grid_sizer_1.Add(
				self.destination_dir_picker, 1, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.EXPAND | wx.TOP, 3
				)
		sizer_2.Add(grid_sizer_1, 1, wx.EXPAND, 0)
		static_line_2 = wx.StaticLine(self.panel_1, wx.ID_ANY)
		sizer_2.Add(static_line_2, 0, wx.BOTTOM | wx.EXPAND | wx.TOP, 5)
		move_or_copy_label = wx.StaticText(self.panel_1, wx.ID_ANY, "Would you like to copy or move the images?")
		sizer_2.Add(move_or_copy_label, 0, 0, 0)
		sizer_2.Add(self.copy_radio_btn, 0, wx.BOTTOM | wx.TOP, 3)
		sizer_2.Add(self.move_radio_btn, 0, wx.BOTTOM | wx.TOP, 3)
		static_line_3 = wx.StaticLine(self.panel_1, wx.ID_ANY)
		sizer_2.Add(static_line_3, 0, wx.BOTTOM | wx.EXPAND | wx.TOP, 5)
		other_options_label = wx.StaticText(self.panel_1, wx.ID_ANY, "Other Options")
		sizer_2.Add(other_options_label, 0, 0, 0)
		sizer_2.Add(self.within_dirs_checkbox, 0, wx.BOTTOM | wx.TOP, 3)
		sizer_2.Add(self.datetime_checkbox, 0, wx.BOTTOM | wx.TOP, 3)
		sizer_2.Add(self.camera_checkbox, 0, wx.BOTTOM | wx.TOP, 3)
		sizer_2.Add(self.manage_cameras_btn, 0, wx.LEFT, 5)
		static_line_4 = wx.StaticLine(self.panel_1, wx.ID_ANY)
		sizer_2.Add(static_line_4, 0, wx.BOTTOM | wx.EXPAND | wx.TOP, 10)
		sizer_2.Add(self.progress_gauge, 0, wx.EXPAND, 0)
		file_count_text = wx.StaticText(self.panel_1, wx.ID_ANY, "Ready to Sort", style=wx.ALIGN_LEFT)
		progress_text.Add(file_count_text, 1, wx.EXPAND, 0)
		time_elapsed_text = wx.StaticText(self.panel_1, wx.ID_ANY, "0:00:00", style=wx.ALIGN_RIGHT)
		progress_text.Add(time_elapsed_text, 1, wx.EXPAND, 0)
		sizer_2.Add(progress_text, 1, wx.EXPAND, 0)
		static_line_5 = wx.StaticLine(self.panel_1, wx.ID_ANY)
		sizer_2.Add(static_line_5, 0, wx.BOTTOM | wx.EXPAND | wx.TOP, 5)
		self.panel_1.SetSizer(sizer_2)
		sizer_1.Add(self.panel_1, 1, wx.ALL | wx.EXPAND, 10)
		sizer_7.Add(self.cancel_btn, 0, wx.RIGHT, 7)
		sizer_7.Add(self.sort_btn, 0, wx.RIGHT, 7)
		sizer_1.Add(sizer_7, 0, wx.ALIGN_RIGHT | wx.BOTTOM | wx.LEFT | wx.RIGHT, 10)
		self.SetSizer(sizer_1)
		self.Layout()
		# end wxGlade

		self.file_count_text = file_count_text
		self.max_file_count = 0
		self.current_file_count = 0

		self.time_elapsed_text = time_elapsed_text
		self.elapsed_time = 0

	def set_max_file_count(self, value: int):
		"""
		Set total number of files to be sorted

		:param value: total number of files to be sorted
		"""

		self.max_file_count = value
		self.progress_gauge.SetRange(value)
		self.update_file_count()

	def reset_file_count(self):
		"""
		Reset count of files that have been sorted to 0
		"""

		self.current_file_count = 0
		self.update_file_count()

	def update_file_count(self, *_):
		"""
		Update tracker to show new count of files that have been sorted
		"""

		self.file_count_text.SetLabel(f"Processing {self.current_file_count} of {self.max_file_count}")
		self.progress_gauge.SetValue(self.current_file_count)

	def increase_file_count(self, *_):
		"""
		Increase count of files that have been sorted
		"""

		self.current_file_count += 1
		self.update_file_count()

	def on_sort_done(self, *_):
		"""
		Tidy up after all files have been sorted
		"""

		self.timer.join()
		self.sort_btn.Enable()
		self.cancel_btn.SetLabel("Close")

		label = f"Complete: {self.current_file_count} file{'s' if self.current_file_count > 1 else ''} sorted"
		self.file_count_text.SetLabel(label)
		wx.MessageDialog(self, "Sort Complete", "Sort Complete", style=wx.OK | wx.ICON_INFORMATION).ShowModal()

	def update_time_elapsed(self, *_):
		"""
		Increase elapsed time by one and update display
		"""

		self.elapsed_time += 1
		self.time_elapsed_text.SetLabel(f"{timedelta(seconds=self.elapsed_time)}")
		self.Layout()

	def do_manage_cameras(self, event):  # wxGlade: Launcher.<event_handler>
		"""
		Handler for ``Manage Cameras`` button.

		Opens ``Manage Cameras`` dialog.
		"""

		with ManageCameras(self, data=self.cameras) as dlg:
			res = dlg.ShowModal()
			if res == wx.ID_APPLY:
				self.cameras = dlg.get_data()
				print(self.cameras)

		event.Skip()

	def within_dirs_ignore(self, event):
		event.Skip()

	def within_dirs_folder_done(self, event):
		"""
		Tidy up after all files have been sorted with `within_dirs=True`
		"""

		event.Skip()

		self.increase_file_count()

		if self.current_file_count == self.max_file_count:
			self.timer.join()
			self.sort_btn.Enable()
			self.cancel_btn.SetLabel("Close")

			label = f"Complete: {self.current_file_count} file{'s' if self.current_file_count > 1 else ''} sorted"
			self.file_count_text.SetLabel(label)
			wx.MessageDialog(self, "Sort Complete", "Sort Complete", style=wx.OK | wx.ICON_INFORMATION).ShowModal()

			# Reset event bindings
			progress_event.Unbind()
			sorting_done.Unbind()

			progress_event.Bind(self.increase_file_count)
			sorting_done.Bind(self.increase_file_count)

	def sort_within_dirs(self):
		"""
		Run sort within folders
		"""

		# Rebind events
		progress_event.Unbind()
		sorting_done.Unbind()

		progress_event.Bind(self.within_dirs_ignore)
		sorting_done.Bind(self.within_dirs_folder_done)

		main_source = self.source_dir_picker.get_value()
		print(f"Main Source: {main_source}")

		subdir_list = [x[0] for x in os.walk(main_source)]
		self.set_max_file_count(len(subdir_list))
		# TODO: Handle no folders
		print(subdir_list)

		if len(subdir_list) >= 1:
			for subdir in subdir_list:
				print(f"Subdir: {subdir}")

				print(os.path.split(subdir)[-1])

				onlyfiles = []

				print(f"Source: {subdir}")

				for root, dirs, files in os.walk(subdir):
					for filename in os.listdir(root):
						if os.path.isfile(os.path.join(root, filename)):
							onlyfiles.append(os.path.join(root, filename))

				print(onlyfiles)

				if self.copy_radio_btn.GetValue() and not self.move_radio_btn.GetValue():
					mode = mode_copy
				elif self.move_radio_btn.GetValue() and not self.move_radio_btn.GetValue():
					mode = mode_move
				else:
					mode = mode_copy

				self.elapsed_time = 0

				self.worker = Worker(
						self,
						filelist=onlyfiles,
						destination=subdir,
						mode=mode,  # TODO: Disable copy checkbox if within dirs selected
						within_dirs=True,
						by_datetime=self.datetime_checkbox.GetValue(),
						by_camera=self.camera_checkbox.GetValue(),
						)
				self.timer = Timer(self)
				self.timer.start()
				self.worker.start()

	def sort(self) -> None:  # wxGlade: Launcher.<event_handler>
		"""
		Run sort.
		"""

		onlyfiles = []

		source = self.source_dir_picker.get_value()
		print(f"Source: {source}")

		for root, dirs, files in os.walk(source):
			for filename in os.listdir(root):
				if os.path.isfile(os.path.join(root, filename)):
					onlyfiles.append(os.path.join(root, filename))

		print(onlyfiles)
		self.reset_file_count()
		self.set_max_file_count(len(onlyfiles))
		# TODO: Handle no files

		if self.copy_radio_btn.GetValue() and not self.move_radio_btn.GetValue():
			mode = mode_copy
		elif self.move_radio_btn.GetValue() and not self.copy_radio_btn.GetValue():
			mode = mode_move
		else:
			mode = mode_copy

		self.elapsed_time = 0

		self.worker = Worker(
				self,
				filelist=onlyfiles,
				destination=self.destination_dir_picker.get_value(),
				mode=mode,
				within_dirs=self.within_dirs_checkbox.GetValue(),
				by_datetime=self.datetime_checkbox.GetValue(),
				by_camera=self.camera_checkbox.GetValue(),
				)
		self.timer = Timer(self)
		self.timer.start()
		self.worker.start()

	def sort_handler(self, event) -> None:  # wxGlade: Launcher.<event_handler>
		"""
		Handler for sort button do determine which function
		to call depending on options selected by the user
		"""

		self.sort_btn.Disable()
		self.cancel_btn.SetLabel("Cancel")

		if self.within_dirs_checkbox.GetValue():
			self.sort_within_dirs()
		else:
			self.sort()

		event.Skip()

	def stop_threads(self) -> None:
		"""
		Stop worker and timer threads.
		"""

		try:
			self.worker.join()
		except AttributeError:
			pass

		try:
			self.timer.join()
		except AttributeError:
			pass

	def on_close(self, event) -> None:  # wxGlade: Launcher.<event_handler>
		"""
		Handler for closing the window.
		"""

		if worker_thread_running:
			res = wx.MessageDialog(
					self,
					"Are you sure you want to cancel?",
					"Cancel?",
					style=wx.YES_NO | wx.ICON_QUESTION,
					).ShowModal()
			if res == wx.ID_NO:
				if event.CanVeto:
					event.Veto()
					return
			self.stop_threads()

		# Save camera and directory settings
		with open("settings.json", 'w') as f:
			json.dump([
					self.cameras,
					{
							"Source": self.source_dir_picker.GetValue(),
							"Destination": self.destination_dir_picker.GetValue(),
							}
					],
						f)

		self.Destroy()  # you may also do:  event.Skip()
		# since the default event handler does call Destroy(), too

	def on_cancel(self, *args):  # wxGlade: Launcher.<event_handler>
		"""
		Handler for cancel/close button, depending on context
		"""

		if worker_thread_running:
			res = wx.MessageDialog(
					self, "Are you sure you want to cancel?", "Cancel?", style=wx.YES_NO | wx.ICON_QUESTION
					).ShowModal()
			if res == wx.ID_YES:
				self.stop_threads()
				self.timer.join()
				self.sort_btn.Enable()
				self.cancel_btn.SetLabel("Close")

		if self.cancel_btn.Label == "Close":
			self.Close()

	def within_dirs_clicked(self, event) -> None:  # wxGlade: Launcher.<event_handler>
		"""
		Handler for ``within_dirs`` checkbox being toggled.
		"""

		self.destination_dir_picker.Enable(not self.destination_dir_picker.IsEnabled())
		self.move_radio_btn.SetValue(1)
		self.move_radio_btn.Enable(not self.move_radio_btn.IsEnabled())
		self.copy_radio_btn.SetValue(0)
		self.copy_radio_btn.Enable(not self.copy_radio_btn.IsEnabled())

		event.Skip()

	def set_settings_file(self, event) -> None:  # wxGlade: Launcher.<event_handler>
		dlg = SettingsDialog(self, id=wx.ID_ANY)
		res = dlg.ShowModal()
		print("Event handler 'set_settings_file' not implemented!")
		event.Skip()


# end of class Launcher
