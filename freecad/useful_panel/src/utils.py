import FreeCAD as App
import re

cell_regex = re.compile("^[A-Z]+[0-9]+$")

# def message(txt):
# 	msg = QtGui.QMessageBox()
# 	msg.setText(str(txt))
# 	msg.exec()

def monospace(text):
	return "<pre>" + text + "</pre>"

def get_all_objects(search_global):
	objects = []
	docs = []
	if (search_global):
		docs = App.listDocuments().values() #type:ignore
	else:
		docs = [App.ActiveDocument]

	for doc in docs:
		for obj in doc.Objects:
			objects.append((doc.Name, obj))
	return objects


def search_for_expressions(w_spreadsheet, search_global, callback=None):
	if callback is None:
		return  # should never happen
	objects = get_all_objects(search_global)
	i=0
	for doc, o in objects:
		if hasattr(o, "ExpressionEngine"):
			for exp in o.ExpressionEngine:
				callback(i, doc, o, exp[0], exp[1])
		if o.TypeId == "Spreadsheet::Sheet" and w_spreadsheet:
			for cell in filter(cell_regex.search, o.PropertiesList):
				contents=o.getContents(cell)
				if contents.startswith("="):
					callback(i, doc, o, cell, contents)
		i += 1
