


import os
import __main__
import FreeCAD as App
import Mesh
from PySide import QtCore, QtGui
from .utils import get_all_objects
from pathlib import Path

class ExportTab(QtGui.QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		export_layout = QtGui.QFormLayout(self)
		export_layout.setContentsMargins(QtCore.QMargins(0, 5, 0, 5))

		export_type = QtGui.QLineEdit("stl")
		self.export_type = export_type
		export_layout.addRow("Export File Type", export_type) # type: ignore

		self.export_location = QtGui.QLineEdit("exports")
		export_layout.addRow("Export Location", self.export_location) # type: ignore

		button_layout = QtGui.QHBoxLayout(self)
		button_layout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))

		export_all_marked_button = QtGui.QPushButton("Export All Marked")
		self.export_all_marked_button = export_all_marked_button
		export_all_marked_button.setToolTip("To Mark a part for exporting, it's `Label2` property must include the word `Export`/`export`.")
		export_all_marked_button.clicked.connect(self.export_all_marked)
		button_layout.addWidget(export_all_marked_button)

		search_globally = QtGui.QCheckBox("From All Documents")
		self.search_globally = search_globally
		button_layout.addWidget(search_globally)
		search_globally.setChecked(False)

		export_layout.addRow(button_layout)

		self.results = []

	def export_all_marked(self):
		export_location = self.export_location.text()
		export_type = self.export_type.text()
		search_globally = self.search_globally.checkState()
		objects = get_all_objects(search_globally)
		cannot_export = []
		for doc, obj in objects:
			if "Export" in obj.Label2 or "export" in obj.Label2:
				try:
					obj.touch()
				except Exception as e:
					print(e)
					cannot_export.append(obj)
		App.ActiveDocument.recompute()
		current_dir = os.path.dirname(App.ActiveDocument.FileName)
		for doc, obj in objects:
			if "Export" in obj.Label2 or "export" in obj.Label2:
				obj_name = doc + "-" + obj.Label
				if (obj in cannot_export):
					print(obj_name + "has errors, cannot export.")
					continue
				directory = os.path.join(current_dir, export_location + "/")
				filename = os.path.join(directory + obj_name + "." + export_type)
				Path(directory).mkdir(parents=True, exist_ok=True)
				try:
					if os.path.exists(filename):
						os.remove(filename)

					print("Exported: " + filename)
				except Exception as e:
					print("Failed to export :" + obj_name)
					print(e)
