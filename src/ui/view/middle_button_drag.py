from PyQt5.QtCore    import Qt
from PyQt5.QtGui     import QMouseEvent
from PyQt5.QtWidgets import QGraphicsView, QApplication

import cst

class MiddleButtonDragView(QGraphicsView):
	"""
	This class creates a QGraphicView with middle mouse button drag and mouse wheel zoom
	"""

	def __init__(self, parent = None):
		super(MiddleButtonDragView, self).__init__(parent)
		self.base = 1.0015

	# def mouseReleaseEvent(self, event):
	# 	super(MiddleButtonDragView, self).mouseReleaseEvent(event)
	# 	print(self.transform().dx(), self.transform().dx())

	def mousePressEvent(self, event):
		if cst.behavior["view"]["drag"](event.buttons(), QApplication.keyboardModifiers()):
			# Hack for middle mouse button adapted from https://gist.github.com/Legor/a00760b6d7af32c01357fb7ff76ad86a
			self.setDragMode(QGraphicsView.ScrollHandDrag)
			fake_event = QMouseEvent(event.type(), event.localPos(), event.windowPos(), event.screenPos(), Qt.LeftButton, event.buttons(), event.modifiers())
			super(MiddleButtonDragView, self).mousePressEvent(fake_event)

	def mouseReleaseEvent(self, event):
		# if cst.behavior["view"]["drag"](event.buttons(), QApplication.keyboardModifiers()):
		self.scene.update()
		self.setDragMode(QGraphicsView.NoDrag)

	def wheelEvent(self,event):
		# global event_bu
		zoomInFactor = 1.25
		zoomOutFactor = 1 / zoomInFactor

		# Save the scene pos
		oldPos = self.mapToScene(event.pos())

		# Zoom
		if event.angleDelta().y() > 0:
		    zoomFactor = zoomInFactor
		else:
		    zoomFactor = zoomOutFactor
		self.scale(zoomFactor, zoomFactor)

		# Get the new position
		newPos = self.mapToScene(event.pos())

		# Move scene to old position
		delta = newPos - oldPos
		self.translate(delta.x(), delta.y())

