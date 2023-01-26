
from PySide import QtCore, QtGui

from freecad.useful_panel.src.SelectionInfo import SelectionInfo
from freecad.useful_panel.src.SearchTab import SearchTab
from freecad.useful_panel.src.ExportTab import ExportTab

class MainWidget(QtGui.QWidget):
	selection_info: SelectionInfo
	def __init__(self):
		super(MainWidget, self).__init__() # type: ignore
		self.main_layout = QtGui.QVBoxLayout(self)
		self.main_layout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))

		self.selection_info = SelectionInfo(self.main_layout)

		tab_widget = QtGui.QTabWidget()
		self.main_layout.addWidget(tab_widget)
		collapse_tabs = QtGui.QWidget()
		tab_widget.addTab(collapse_tabs, "^")  # type: ignore
		search_tab = SearchTab()
		tab_widget.addTab(search_tab, "Search/Replace")  # type: ignore
		export_tab = ExportTab()
		tab_widget.addTab(export_tab, "Batch Export")  # type: ignore

class MainPanel(QtGui.QDockWidget):
	def __init__(self):
		super(MainPanel, self).__init__() # type: ignore
		self.initUI()

	def initUI(self):
		self.setWindowTitle("Useful Panel")
		self.setObjectName("Useful Panel") #required to restore panel
		self.main_widget = MainWidget()
		# todo fix this passing down selection info mess
		self.selection_info = self.main_widget.selection_info
		self.setWidget(self.main_widget)
	def toggle(self):
		if (self.isVisible()):
			self.hide()
		else:
			self.show()
		return
