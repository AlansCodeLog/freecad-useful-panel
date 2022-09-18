FreeCAD addon that does several useful things (am too lazy to create seperate addons):

![](./attachments/Screenshot.png)

- Displays the current selection length.
- Displays the distances between any two selections (similar to [Part Measure Linear](https://wiki.freecad.org/Part_Measure_Linear)).
	- Plus additional X/Y/Z Min/Max measurements (i.e. the difference between the bounding edges of the selection). Sometimes the distance between two selections can be zero, but different size (e.g. two circles on top of each other, but their diameters are different). The min/max distances show this.
	
https://user-images.githubusercontent.com/26168490/190905158-77e2890d-12f2-4be0-8a0a-e1d9850efb63.mp4


- Provides a way to find and replace text in expressions. Either in all documents, or only the current. Can also optionally replace text in spreadsheets.
	- Incredibly useful if you have a lot of variables and like to rename things.
	- Has a preview of the replace text, and matches can be omitted via a checkbox.
	- **CAREFUL:** This is a simple text replacement, and the outputted expression is not guaranteed to be valid.

- Provides a way to export all "marked" objects. Marking is done by including the word "Export" in the part's `Label2` property.
	- Path is relative to the active document. Parts are named `{file name}-{object name}.{extension}`.
	- **The file is always overwritten if it exists.**

### Notes

- I suggest disabling loading partial documents if using replace in all documents. (`General => Document => Document objects => Disable partial loading of external linked objects`). I've not tested this with partially loaded docs and I've had problems with them with other addons so don't use partial loading.

### Todos

- [ ] At some point I would like to see if it's possible to move the measurements to the viewport a la Fusion360.

### Development

```sh
python3 -m venv .venv
pip install -r requirements

```
For intellisence create `.env` with:
Note: Something is still off / not completely working with PySide impports...

```
FREECAD_LIB=/usr/lib/freecad/lib
FREECAD_MOD=/path/to/Mod
FREECAD_STUBS=/path/to/stubs (e.g. generated with freecad-stubs)
FREECAD_EXT=/usr/lib/freecad/Ext
PYTHONPATH=${FREECAD_MOD}:${FREECAD_LIB}:${FREECAD_EXT}:${PYTHONPATH}
```
