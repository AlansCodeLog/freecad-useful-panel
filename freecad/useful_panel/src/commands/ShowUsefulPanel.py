import os
from freecad.useful_panel.src.MainPanel import MainPanel
from freecad.useful_panel import ICONPATH

class ShowUsefulPanel():
	"""Show Useful Panel"""
	def __init__(self, main_panel: MainPanel):
		self.main_panel = main_panel

	def GetResources(self):
		return {"Pixmap":  os.path.join(ICONPATH, "icon.svg"),
				"MenuText": "Show Useful Panel",
				"ToolTip": ""}

	def Activated(self):
		self.main_panel.toggle()
