

import __main__
import FreeCADGui as Gui

test = False # for intellisense arrafasdfasdf
def usefulPanelsMain(name):
	if name == "NoneWorkbench":
		return
	import __main__
	Gui.getMainWindow().workbenchActivated.disconnect(__main__.usefulPanelMain)

	import math
	import re

	from PySide import QtCore, QtGui


	cell_regex = re.compile("^[A-Z]+[0-9]+$")
	def monospace(text):
		return "<pre>"+text+"</pre>"
	class MainWidget(QtGui.QWidget):

		def __init__(self):
			super(MainWidget, self).__init__()

			super().setWindowTitle("Useful Panel")
			super().setObjectName("Useful Panel")

			self.initUI()

		def initUI(self):
			self.layout = QtGui.QVBoxLayout()
			self.layout.setContentsMargins(0, 0, 0, 0)
			# sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
			# sld.setFocusPolicy(QtCore.Qt.NoFocus)
			# sld.setRange(1, 750)
			# sld.setValue(75)
			# sld.valueChanged.connect(self.sliderChanged)

			# self.layout.addWidget(sld)
			self.countTitleLabel = QtGui.QLabel(monospace("Selection Count: 0"))
			self.layout.addWidget(self.countTitleLabel)

			self.countLabel = QtGui.QLabel("")
			self.countLabel.setVisible(False)
			self.layout.addWidget(self.countLabel)

			self.distanceLabel = QtGui.QLabel("")
			self.distanceLabel.setVisible(False)
			self.layout.addWidget(self.distanceLabel)

			self.search_layout = QtGui.QFormLayout()
			self.search_layout.setContentsMargins(0, 0, 0, 0)
			self.layout.addLayout(self.search_layout)

			self.aliasResultLabel = QtGui.QLabel("Search for Alias")
			self.aliasSearchTerm = QtGui.QLineEdit("")
			self.search_layout.addRow(self.aliasResultLabel, self.aliasSearchTerm)
			self.aliasSearchTerm.textChanged.connect(self.searchAlias)

			self.aliasReplaceLabel = QtGui.QLabel("Replace Alias With")
			self.aliasReplaceTerm = QtGui.QLineEdit("")
			self.search_layout.addRow(self.aliasReplaceLabel, self.aliasReplaceTerm)
			self.aliasReplaceTerm.textChanged.connect(self.searchAlias)

			self.options_layout = QtGui.QHBoxLayout()
			self.options_layout.setContentsMargins(0, 0, 0, 0)

			self.aliasSearchGlobal = QtGui.QCheckBox("Search All Documents")
			self.options_layout.addWidget(self.aliasSearchGlobal)
			self.aliasSearchGlobal.setChecked(True)
			self.aliasSearchGlobal.stateChanged.connect(self.searchAlias)

			self.includeSpreadsheet = QtGui.QCheckBox("Include Spreadsheets")
			self.options_layout.addWidget(self.includeSpreadsheet)
			self.includeSpreadsheet.setChecked(True)
			self.includeSpreadsheet.stateChanged.connect(self.searchAlias)

			self.search_layout.addRow(self.options_layout)


			# BUTTONS
			self.buttons_layout = QtGui.QHBoxLayout()
			self.buttons_layout.setContentsMargins(0, 0, 0, 0)

			self.aliasCheckAllButton = QtGui.QPushButton("Check All")
			self.buttons_layout.addWidget(self.aliasCheckAllButton)
			self.aliasCheckAllButton.clicked.connect(self.checkAll)

			self.aliasUncheckAllButton = QtGui.QPushButton("Uncheck All")
			self.buttons_layout.addWidget(self.aliasUncheckAllButton)
			self.aliasUncheckAllButton.clicked.connect(self.uncheckAll)

			self.aliasReplaceButton = QtGui.QPushButton("Replace")
			self.buttons_layout.addWidget(self.aliasReplaceButton)
			self.aliasReplaceButton.clicked.connect(self.replaceAlias)

			self.search_layout.addRow(self.buttons_layout)


			self.aliasResultsTable = QtGui.QTableWidget()
			self.aliasResultsTable.setHorizontalHeaderLabels(
				("Object", "Property", "Expression"))
			sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
			sizePolicy.setHorizontalStretch(1)
			sizePolicy.setVerticalStretch(1)
			self.aliasResultsTable.setSizePolicy(sizePolicy)
			self.aliasResultsTable.horizontalHeader().setStretchLastSection(True)
			self.aliasResultsTable.horizontalHeader().setDefaultSectionSize(100)
			self.aliasResultsTable.setWordWrap(True)

			self.aliasResultsTable.horizontalHeader().sectionResized.connect(self.resizeRows)

			self.layout.addWidget(self.aliasResultsTable)


			# spacer = verticalSpacer = QtGui.QSpacerItem(
			# 	0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
			# self.layout.addItem(spacer)

			self.other_layout = QtGui.QFormLayout()
			self.other_layout.setContentsMargins(0, 0, 0, 0)
			self.layout.addLayout(self.other_layout)

			self.exportTypeLabel = QtGui.QLabel("Export File Type")
			self.exportType = QtGui.QLineEdit("")
			self.exportType.setText("stl")
			self.other_layout.addRow(self.exportTypeLabel, self.exportType)

			self.exportLocationLabel = QtGui.QLabel("Export Location")
			self.exportLocation = QtGui.QLineEdit("")
			self.exportLocation.setText("exports")
			self.other_layout.addRow(self.exportLocationLabel, self.exportLocation)

			self.exportAllMarkedButton = QtGui.QPushButton("Export All Marked")
			self.exportAllMarkedButton.setToolTip("To Mark a part for exporting, it's `Label2` property must include the word `Export`/`export`.")
			self.other_layout.addRow(self.exportAllMarkedButton)
			self.exportAllMarkedButton.clicked.connect(self.exportAllMarked)

			self.setLayout(self.layout)


		def resizeRows(self):
			self.aliasResultsTable.resizeRowsToContents()
		def getAllObjects(self):
			search_global = self.aliasSearchGlobal.checkState()
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

		def searchForExpressions(self, callback=None):
			objects = self.getAllObjects()
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


		def exportAllMarked(self):
			exportLocation = self.exportLocation.text()
			exportType = self.exportType.text()
			objects = self.getAllObjects()
			for doc, obj in objects:
				if "Export" in obj.Label2 or "export" in obj.Label2:
					filename = exportLocation + "/" + doc + "-" + obj.Label + "." + exportType
					command = "export" + exportType.capitalize()
					func = getattr(obj.Shape, command)
					func(filename)
					print("Exported: "+ filename)

		def checkAll(self):
			replacement = self.aliasReplaceTerm.text()
			show_replace = len(replacement) > 0
			if show_replace:
				for i in range(self.aliasResultsTable.rowCount()):
					cell = self.aliasResultsTable.cellWidget(i, 0)
					cell.setChecked(True)

		def uncheckAll(self):
			replacement = self.aliasReplaceTerm.text()
			show_replace = len(replacement) > 0
			if show_replace:
				for i in range(self.aliasResultsTable.rowCount()):
					cell = self.aliasResultsTable.cellWidget(i, 0)
					cell.setChecked(False)

		def replaceAlias(self):
			name = self.aliasSearchTerm.text()
			replacement = self.aliasReplaceTerm.text()
			w_spreadsheet = self.includeSpreadsheet.checkState()
			def search(i, doc, o, prop, exp):
				cell = self.aliasResultsTable.cellWidget(i, 0)
				if cell.checkState() == False:
					return
				if name in exp:
					new_expression = exp.replace(name, replacement)
					if o.TypeId == "Spreadsheet::Sheet" and w_spreadsheet:
						o.set(prop, new_expression)
					else:
						o.setExpression(prop, new_expression)

			self.searchForExpressions(search)

			self.searchAlias()  # refresh

		def searchAlias(self):
			name = self.aliasSearchTerm.text()
			replacement = self.aliasReplaceTerm.text()
			search_global = self.aliasSearchGlobal.checkState()
			found = []
			show_replace = len(replacement) > 0
			objects = self.getAllObjects()

			def search(i, doc, o, prop, exp):
				if name in exp:
					item = [doc, o.Label, prop, exp]
					if show_replace:
						item.append(exp.replace(name, replacement))
					found.append(item)

			self.searchForExpressions(search)


			header = ["Obj", "Prop", "Exp"]
			addColumn = 0
			if search_global:
				header.insert(0, "Doc")
			if show_replace:
				header.insert(0, "[ ]")
				header.insert(len(header), "Replacement")
				addColumn = 1

			sameCols = self.aliasResultsTable.columnCount() == len(header)
			sameRows = self.aliasResultsTable.rowCount() == len(found)

			if not sameCols:
				self.aliasResultsTable.clear()
			self.aliasResultsTable.setRowCount(len(found))
			self.aliasResultsTable.setColumnCount(len(header))
			self.aliasResultsTable.setHorizontalHeaderLabels(tuple(header))

			for row, item in enumerate(found):
				if show_replace and (not sameCols or not sameRows):
					checkbox = QtGui.QCheckBox("")
					checkbox.setChecked(True)
					self.aliasResultsTable.setCellWidget(row, 0, checkbox)
				for col, part in enumerate(item):
					newItem = QtGui.QTableWidgetItem(part)
					self.aliasResultsTable.setItem(row, col+addColumn, newItem)

			if show_replace:
				self.aliasResultsTable.setColumnWidth(0, 10)

			self.aliasResultsTable.resizeRowsToContents()
			# self.aliasResultsTable.resizeColumnsToContents()

		def setSelectionInfo(self,
                       count,
                       sum,
                       distances
                       ):
			self.countTitleLabel.setText(monospace("Selection Count:" +count))
			self.countLabel.setText(monospace(sum + "mm Selected"))
			self.countLabel.setVisible(True)
			if distances != None:
				self.distanceLabel.setVisible(True)
				(distance, x_distance, y_distance, z_distance, xmin_distance, ymin_distance, zmin_distance, xmax_distance, ymax_distance, zmax_distance) = distances
				# longest_normal = len(min([x_distance, y_distance, z_distance], key=lambda x: len(x)))
				# longest_min = len(min([xmin_distance, ymin_distance, zmin_distance], key=lambda x: len(x)))
				# longest_max = len(min([xmax_distance, ymax_distance, zmax_distance], key=lambda x: len(x)))
				self.distanceLabel.setText(monospace(
					"Distance: " + distance + "mm" + "\n" +
					"X " + x_distance + "mm (Min " + xmin_distance + "mm, Max " + xmax_distance + "mm)" + "\n" +
					"Y " + y_distance + "mm (Min " + ymin_distance + "mm, Max " + ymax_distance + "mm)" + "\n" +
					"Z " + z_distance + "mm (Min " + zmin_distance + "mm, Max " + zmax_distance + "mm)" + "\n"
				))
			else:
				self.distanceLabel.setText("")
				self.distanceLabel.setVisible(False)

		def setNoSelection(self):
			self.countTitleLabel.setText(monospace("Selection Count: 0"))
			# self.countLabel.setText(monospace("0 mm Selected"))
			self.countLabel.setVisible(False)
			self.distanceLabel.setVisible(False)

		def sliderChanged(self, value):
			# print(value)
			return

	class SelectionObserver:
		def __init__(self, widget):
			self.widget = widget
			self.disableObserver = False

		def addSelection(self, doc, obj, sub, pnt):
			self.checkSelection()

		def removeSelection(self, doc, obj, sub):
			self.checkSelection()

		def setSelection(self, doc):
			self.checkSelection()

		def clearSelection(self, doc):
			self.checkSelection()

		def checkSelection(self):
			selections = Gui.Selection.getSelectionEx()

			# def message(txt):
			# 	msg = QtGui.QMessageBox()
			# 	msg.setText(str(txt))
			# 	msg.exec()

			def round_to(n, x = 1000):
				return "{:.3f}".format(math.ceil(n * x) / x)
				# return math.ceil(n * x) / x

			ok = False
			if len(selections) == 0:
				self.widget.setNoSelection()
			else:
				selection = [item for selection in selections for item in selection.SubObjects]

				if len(selection) == 0:
					self.widget.setNoSelection()
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

					distances = (distance, x_distance, y_distance, z_distance, xmin_distance,
					             ymin_distance, zmin_distance, xmax_distance, ymax_distance, zmax_distance)

				self.widget.setSelectionInfo(
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
__main__.usefulPanelMain = usefulPanelsMain

# Connect the function that runs the macro to the appropriate signal
Gui.getMainWindow().workbenchActivated.connect(usefulPanelMain)
