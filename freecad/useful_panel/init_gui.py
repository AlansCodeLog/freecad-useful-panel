import os
from freecad.useful_panel import ICONPATH
from freecad.useful_panel.src.MainPanel import MainPanel
import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtCore, QtGui
import __main__

from freecad.useful_panel.src.ViewportWidget import ViewportWidget

class UsefulPanelWorkbench(Gui.Workbench):
	"""
	Useful Panel Workbench
	"""

	MenuText = "Useful Panel"
	ToolTip = "Useful"
	Icon = os.path.join(ICONPATH, "icon.svg")
	toolbox = ["ShowUsefulPanel"]

	def GetClassName(self):
		return "Gui::PythonWorkbench"

	def Initialize(self):
		from freecad.useful_panel.src.commands.ShowUsefulPanel import ShowUsefulPanel

		App.Console.PrintMessage("Initializing Useful Panel Workbench\n") # type: ignore

		self.main_panel:MainPanel = __main__.main_panel

		Gui.addCommand("ShowUsefulPanel", ShowUsefulPanel(self.main_panel))

		self.appendToolbar("UsefulPanel", self.toolbox)
		self.appendMenu("UsefulPanel", self.toolbox)
		mw = Gui.getMainWindow()
		tw = ViewportWidget(mw)

	def Activated(self):
		self.main_panel.show()
		App.Console.PrintMessage("Activated Useful Panel Workbench\n") # type: ignore
		pass

	def Deactivated(self):
		pass

# this allows the panel position to saved/restored
__main__.main_panel = MainPanel() # type: ignore
Gui.Selection.addObserver(__main__.main_panel.selection_info.observer)  # type: ignore

mw = Gui.getMainWindow()
mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, __main__.main_panel)
Gui.addWorkbench(UsefulPanelWorkbench())# type:ignore
