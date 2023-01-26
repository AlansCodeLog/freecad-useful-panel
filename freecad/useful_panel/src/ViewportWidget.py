from pivy import coin
from PySide import QtGui
from PySide.QtCore import Qt
from PySide.QtGui import QPainter,QApplication, QMainWindow, QWidget
import FreeCADGui as Gui
class ViewportWidget():
    def __init__(self, mw):

        # setup the contour
        color = coin.SoBaseColor()
        color.rgb = (1, 0, 0)

        points = coin.SoCoordinate3()
        lines = coin.SoLineSet()

        points.point.values = ((0, 0, 0), (10, 10, 10), (10, 10, 0))


        # feed data to separator
        sep = coin.SoSeparator()
        sep.addChild(points)
        sep.addChild(color)
        sep.addChild(lines)

        # add separator to sceneGraph
        sg = Gui.ActiveDocument.ActiveView.getSceneGraph()
        sg.addChild(sep)

    # def __init__(self, parent=None):
    #     super().__init__(parent)
    #     self.setAttribute(Qt.WA_TransparentForMouseEvents)
    #     self.setAttribute(Qt.WA_NoSystemBackground)
    #     self.setAttribute(Qt.WA_TranslucentBackground)
    #     self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    #     self.setMouseTracking(True)
    #     self.drag_position = None

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
    #         event.accept()

    # def mouseMoveEvent(self, event):
    #     if event.buttons() == Qt.LeftButton:
    #         self.move(event.globalPos() - self.drag_position)
    #         event.accept()

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setOpacity(0.5)
    #     painter.fillRect(event.rect(), Qt.white)
