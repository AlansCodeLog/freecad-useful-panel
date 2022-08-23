

import __main__
import FreeCADGui as Gui

# def message(txt):
# 	msg = QtGui.QMessageBox()
# 	msg.setText(str(txt))
# 	msg.exec()

def useful_panels_main(name):
	if name == "NoneWorkbench":
		return
	import __main__
	Gui.getMainWindow().workbenchActivated.disconnect(__main__.useful_panels_main)

	import math
	import re

	from PySide import QtCore, QtGui

	cell_regex = re.compile("^[A-Z]+[0-9]+$")

	def monospace(text):
		return "<pre>" + text + "</pre>"

	class MainWidget(QtGui.QWidget):

		def __init__(self):
			super(MainWidget, self).__init__()

			super().setWindowTitle("Useful Panel")
			super().setObjectName("Useful Panel")

			self.initUI()

		def initUI(self):
			self.main_layout = QtGui.QVBoxLayout()
			self.main_layout.setContentsMargins(0, 0, 0, 0)
			# sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
			# sld.setFocusPolicy(QtCore.Qt.NoFocus)
			# sld.setRange(1, 750)
			# sld.setValue(75)
			# sld.valueChanged.connect(self.sliderChanged)

			# self.main_layout.addWidget(sld)
			self.cont_title_label = QtGui.QLabel(monospace("Selection Count: 0"))
			self.main_layout.addWidget(self.cont_title_label)

			self.count_label = QtGui.QLabel("")
			self.count_label.setVisible(False)
			self.main_layout.addWidget(self.count_label)

			self.distance_label = QtGui.QLabel("")
			self.distance_label.setVisible(False)
			self.main_layout.addWidget(self.distance_label)

			self.search_layout = QtGui.QFormLayout()
			self.search_layout.setContentsMargins(0, 0, 0, 0)
			self.main_layout.addLayout(self.search_layout)

			self.alias_result_label = QtGui.QLabel("Search for Alias")
			self.alias_search_term = QtGui.QLineEdit("")
			self.search_layout.addRow(self.alias_result_label, self.alias_search_term)
			self.alias_search_term.textChanged.connect(self.search_alias)

			self.alias_replace_label = QtGui.QLabel("Replace Alias With")
			self.alias_replace_term = QtGui.QLineEdit("")
			self.search_layout.addRow(self.alias_replace_label, self.alias_replace_term)
			self.alias_replace_term.textChanged.connect(self.search_alias)

			self.options_layout = QtGui.QHBoxLayout()
			self.options_layout.setContentsMargins(0, 0, 0, 0)

			self.alias_search_global = QtGui.QCheckBox("Search All Documents")
			self.options_layout.addWidget(self.alias_search_global)
			self.alias_search_global.setChecked(True)
			self.alias_search_global.stateChanged.connect(self.search_alias)

			self.includeSpreadsheet = QtGui.QCheckBox("Include Spreadsheets")
			self.options_layout.addWidget(self.includeSpreadsheet)
			self.includeSpreadsheet.setChecked(True)
			self.includeSpreadsheet.stateChanged.connect(self.search_alias)

			self.search_layout.addRow(self.options_layout)

			# BUTTONS
			self.buttons_layout = QtGui.QHBoxLayout()
			self.buttons_layout.setContentsMargins(0, 0, 0, 0)

			self.alias_check_all_button = QtGui.QPushButton("Check All")
			self.buttons_layout.addWidget(self.alias_check_all_button)
			self.alias_check_all_button.clicked.connect(self.check_all)

			self.alias_uncheck_all_button = QtGui.QPushButton("Uncheck All")
			self.buttons_layout.addWidget(self.alias_uncheck_all_button)
			self.alias_uncheck_all_button.clicked.connect(self.uncheck_all)

			self.alias_replace_button = QtGui.QPushButton("Replace")
			self.buttons_layout.addWidget(self.alias_replace_button)
			self.alias_replace_button.clicked.connect(self.replace_alias)

			self.search_layout.addRow(self.buttons_layout)

			# Table
			self.alias_results_table = QtGui.QTableWidget()
			self.alias_results_table.setHorizontalHeaderLabels(
				("Object", "Property", "Expression"))
			sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
			sizePolicy.setHorizontalStretch(1)
			sizePolicy.setVerticalStretch(1)
			self.alias_results_table.setSizePolicy(sizePolicy)
			self.alias_results_table.horizontalHeader().setStretchLastSection(True)
			self.alias_results_table.horizontalHeader().setDefaultSectionSize(100)
			self.alias_results_table.setWordWrap(True)

			self.alias_results_table.horizontalHeader().sectionResized.connect(self.resize_rows)

			self.main_layout.addWidget(self.alias_results_table)

			# spacer = verticalSpacer = QtGui.QSpacerItem(
			# 	0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
			# self.main_layout.addItem(spacer)

			self.other_layout = QtGui.QFormLayout()
			self.other_layout.setContentsMargins(0, 0, 0, 0)
			self.main_layout.addLayout(self.other_layout)

			self.export_type_label = QtGui.QLabel("Export File Type")
			self.exportType = QtGui.QLineEdit("")
			self.exportType.setText("stl")
			self.other_layout.addRow(self.export_type_label, self.exportType)

			self.export_location_label = QtGui.QLabel("Export Location")
			self.export_location = QtGui.QLineEdit("")
			self.export_location.setText("exports")
			self.other_layout.addRow(self.export_location_label, self.export_location)

			self.export_all_marked_button = QtGui.QPushButton("Export All Marked")
			self.export_all_marked_button.setToolTip("To Mark a part for exporting, it's `Label2` property must include the word `Export`/`export`.")
			self.other_layout.addRow(self.export_all_marked_button)
			self.export_all_marked_button.clicked.connect(self.export_all_marked)

			self.setLayout(self.main_layout)

		def resize_rows(self):
			self.alias_results_table.resizeRowsToContents()

		def get_all_object(self):
			search_global = self.alias_search_global.checkState()
			objects = []
			docs = []
			if (search_global):
				docs = App.listDocuments().values()
			else:
				docs = [App.ActiveDocument]

			for doc in docs:
				for obj in doc.Objects:
					objects.append((doc.Name, obj))
			return objects

		def search_for_expressions(self, callback=None):
			if callback is None:
				return #should never happen
			objects = self.get_all_object()
			i = 0
			for doc, o in objects:
				if hasattr(o, "ExpressionEngine"):
					for exp in o.ExpressionEngine:
						callback(i, doc, o, exp[0], exp[1])
				if o.TypeId == "Spreadsheet::Sheet":
					for cell in filter(cell_regex.search, o.PropertiesList):
						contents = o.getContents(cell)
						if contents.startswith("="):
							callback(i, doc, o, cell, contents)
				i+=1


		def export_all_marked(self):
			export_location = self.export_location.text()
			export_type = self.exportType.text()
			objects = self.get_all_object()
			for doc, obj in objects:
				if "Export" in obj.Label2 or "export" in obj.Label2:
					objName = doc + "-" + obj.Label
					filename = export_location + "/" + objName + "." + export_type
					command = "export" + export_type.capitalize()
					func = getattr(obj.Shape, command)
					try:
						func(filename)
						print("Exported: "+ filename)
					except Exception as e:
						print("Failed to export :" + objName)
						print(e)

		def check_all(self):
			replacement = self.alias_replace_term.text()
			show_replace = len(replacement) > 0
			if show_replace:
				for i in range(self.alias_results_table.rowCount()):
					cell = self.alias_results_table.cellWidget(i, 0)
					cell.setChecked(True)

		def uncheck_all(self):
			replacement = self.alias_replace_term.text()
			show_replace = len(replacement) > 0
			if show_replace:
				for i in range(self.alias_results_table.rowCount()):
					cell = self.alias_results_table.cellWidget(i, 0)
					cell.setChecked(False)

		def replace_alias(self):
			name = self.alias_search_term.text()
			replacement = self.alias_replace_term.text()
			w_spreadsheet = self.includeSpreadsheet.checkState()
			def search(i, doc, o, prop, exp):
				cell = self.alias_results_table.cellWidget(i, 0)
				if cell.checkState() == False:
					return
				if name in exp:
					new_expression = exp.replace(name, replacement)
					if o.TypeId == "Spreadsheet::Sheet" and w_spreadsheet:
						o.set(prop, new_expression)
					else:
						o.setExpression(prop, new_expression)

			self.search_for_expressions(search)

			self.search_alias()  # refresh

		def search_alias(self):
			name = self.alias_search_term.text()
			replacement = self.alias_replace_term.text()
			search_global = self.alias_search_global.checkState()
			found = []
			show_replace = len(replacement) > 0

			def search(i, doc, o, prop, exp):
				if name in exp:
					item = [doc, o.Label, prop, exp]
					if show_replace:
						item.append(exp.replace(name, replacement))
					found.append(item)

			self.search_for_expressions(search)

			header = ["Obj", "Prop", "Exp"]
			add_column = 0
			if search_global:
				header.insert(0, "Doc")
			if show_replace:
				header.insert(0, "[ ]")
				header.insert(len(header), "Replacement")
				add_column = 1

			same_cols = self.alias_results_table.columnCount() == len(header)
			same_rows = self.alias_results_table.rowCount() == len(found)

			if not same_cols:
				self.alias_results_table.clear()
			self.alias_results_table.setRowCount(len(found))
			self.alias_results_table.setColumnCount(len(header))
			self.alias_results_table.setHorizontalHeaderLabels(tuple(header))

			for row, item in enumerate(found):
				if show_replace and (not same_cols or not same_rows):
					checkbox = QtGui.QCheckBox("")
					checkbox.setChecked(True)
					self.alias_results_table.setCellWidget(row, 0, checkbox)
				for col, part in enumerate(item):
					newItem = QtGui.QTableWidgetItem(part)
					self.alias_results_table.setItem(row, col+add_column, newItem)

			if show_replace:
				self.alias_results_table.setColumnWidth(0, 10)

			self.alias_results_table.resizeRowsToContents()
			# self.aliasResultsTable.resizeColumnsToContents()

		def set_selection_info(self, count, sum, distances):
			self.cont_title_label.setText(monospace("Selection Count:" +count))
			self.count_label.setText(monospace(sum + "mm Selected"))
			self.count_label.setVisible(True)
			if distances is not None:
				self.distance_label.setVisible(True)
				(distance, x_distance, y_distance, z_distance,
				 xmin_distance, ymin_distance, zmin_distance,
				 xmax_distance, ymax_distance, zmax_distance) = distances
				self.distance_label.setText(monospace(
					"Distance: " + distance + "mm" + "\n" +
					"X " + x_distance + "mm (Min " + xmin_distance + "mm, Max " + xmax_distance + "mm)" + "\n" +
					"Y " + y_distance + "mm (Min " + ymin_distance + "mm, Max " + ymax_distance + "mm)" + "\n" +
					"Z " + z_distance + "mm (Min " + zmin_distance + "mm, Max " + zmax_distance + "mm)" + "\n"
				))
			else:
				self.distance_label.setText("")
				self.distance_label.setVisible(False)

		def set_no_selection(self):
			self.cont_title_label.setText(monospace("Selection Count: 0"))
			# self.countLabel.setText(monospace("0 mm Selected"))
			self.count_label.setVisible(False)
			self.distance_label.setVisible(False)

		def slider_changed(self, value):
			# print(value)
			return

	class SelectionObserver:
		def __init__(self, widget):
			self.widget = widget
			self.disableObserver = False

		def addSelection(self, doc, obj, sub, pnt):
			self.check_selection()

		def removeSelection(self, doc, obj, sub):
			self.check_selection()

		def setSelection(self, doc):
			self.check_selection()

		def clearSelection(self, doc):
			self.check_selection()

		def check_selection(self):
			selections = Gui.Selection.getSelectionEx()

			def round_to(n, x=1000):
				return "{:.3f}".format(math.ceil(n * x) / x)
				# return math.ceil(n * x) / x

			ok = False
			selection = []
			if len(selections) == 0:
				self.widget.set_no_selection()
			else:
				selection = [item for selection in selections for item in selection.SubObjects]

				if len(selection) == 0:
					self.widget.set_no_selection()
				else:
					ok = True
			if ok:
				sum = 0
				count = str(len(selection))
				for edge in selection:
					sum += edge.Length

				sum = round_to(sum)

				distances = None
				distance = None
				x_distance = None
				y_distance = None
				z_distance = None
				xmin_distance = None
				ymin_distance = None
				zmin_distance = None
				xmax_distance = None
				ymax_distance = None
				zmax_distance = None

				if len(selection) == 2:
					selcenter1 = selection[0].BoundBox.Center
					selcenter2 = selection[1].BoundBox.Center
					print(selcenter1)
					print(selcenter2)

					distance = round_to(selcenter1.distanceToPoint(selcenter2))
					x_distance = round_to(abs(selcenter1.x - selcenter2.x))
					y_distance = round_to(abs(selcenter1.y - selcenter2.y))
					z_distance = round_to(abs(selcenter1.z - selcenter2.z))

					xmin_distance = round_to(abs(selection[0].BoundBox.XMin - selection[1].BoundBox.XMin))
					xmax_distance = round_to(abs(selection[0].BoundBox.XMax - selection[1].BoundBox.XMax))
					ymin_distance = round_to(abs(selection[0].BoundBox.YMin - selection[1].BoundBox.YMin))
					ymax_distance = round_to(abs(selection[0].BoundBox.YMax - selection[1].BoundBox.YMax))
					zmin_distance = round_to(abs(selection[0].BoundBox.ZMin - selection[1].BoundBox.ZMin))
					zmax_distance = round_to(abs(selection[0].BoundBox.ZMax - selection[1].BoundBox.ZMax))

					distances = (distance, x_distance, y_distance, z_distance,
					             xmin_distance, ymin_distance, zmin_distance,
					             xmax_distance, ymax_distance, zmax_distance)

				self.widget.set_selection_info(
					count, sum, distances)

	app = QtGui.qApp
	mw = Gui.getMainWindow()
	widget = QtGui.QDockWidget()
	widget.setWindowTitle("Useful Panel")
	widget.setObjectName("Useful Panel")
	mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, widget)
	mainWidget = MainWidget()
	widget.setWidget(mainWidget)
	Gui.Selection.addObserver(SelectionObserver(mainWidget))


# The following 2 lines are important because InitGui.py files are passed to the exec() function...
# ...and the runMacro wouldn't be visible outside. So explicitly add it to __main__
__main__.useful_panels_main = useful_panels_main

# Connect the function that runs the macro to the appropriate signal
Gui.getMainWindow().workbenchActivated.connect(useful_panels_main)
