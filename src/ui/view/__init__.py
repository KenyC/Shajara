from PyQt5.QtCore    import Qt, QPoint, QRectF
from PyQt5.QtGui     import QPixmap, QImage, QPolygon, QColor, QBrush, QPen, QPainter
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsView, QGraphicsRectItem

from .middle_button_drag import MiddleButtonDragView
import cst
class TreeObject(QGraphicsItem):


	default_style = {
		"radius_leaves"   : cst.style["nodes"]["radius"], 
		"branch_width"    : cst.style["branches"]["width"], 
		"space_text_node" : cst.style["labels"]["distance_to_node"],
		"font_size"       : cst.style["labels"]["font_size"],
		"color_nodes"     : cst.style["nodes"]["color"], 
		"color_branches"  : cst.style["branches"]["color"], 
		"color_labels"    : cst.style["labels"]["color"]
	}

	infinite_width = 1000

	def __init__(self, tree, **style):
		super(TreeObject, self).__init__()
		self.style = dict(**TreeObject.default_style)
		self.style.update(style)

		self.tree = tree

		self.leaf_brush   = QBrush(QColor(*self.style["color_nodes"]))
		self.branch_pen   = QPen  (QColor(*self.style["color_branches"]))
		self.label_pen    = QPen  (QColor(*self.style["color_labels"]))

		self.branch_pen.setWidth(self.style["branch_width"])

	def paint(self, painter, option, widget):
		if self.tree is not None:
			# self.tree.construct((0, 80))
			label_positions = self.tree.positions


			# Draw branches
			painter.setRenderHint(QPainter.Antialiasing)
			original_pen = painter.pen()
			painter.setPen(self.branch_pen)
			for i in range(self.tree.n):
				if self.tree.children[i]:
					for c in self.tree.children[i]:
						painter.drawLine(
							QPoint(*label_positions[i]), 
							QPoint(*label_positions[c])
						)

			# Draw nodes
			painter.setPen(original_pen)
			painter.setBrush(self.leaf_brush)
			radius = self.style["radius_leaves"]
			for position in label_positions:
				painter.drawEllipse(QPoint(*position), radius, radius)


			# Draw labels
			current_font = painter.font()
			current_font.setPixelSize(self.style["font_size"])
			painter.setFont(current_font)
			painter.setPen(self.label_pen)
			for position, label in zip(label_positions, self.tree.labels):
				if label:# or True:
					painter.drawText(
						QRectF(
							position[0] - TreeObject.infinite_width // 2, 
							position[1], 
							TreeObject.infinite_width, 
							self.style["space_text_node"]
						),
						Qt.AlignCenter | Qt.AlignTop, 
						label
						# "label"
					)

			# painter.drawEllipse(-50, -50, 100, 100)

	def boundingRect(self):
		return QRectF(- 300,- 300, 300, 300)





class TreeView(MiddleButtonDragView):
	"""
	Middle button drag view for QTree contains the tree a graphic item
	"""

	def __init__(self, *args, **kwargs):
		super(TreeView, self).__init__(*args, **kwargs)


		self.scene = TreeScene(self)
		self.setScene(self.scene)
		# This seems to be imperative for drag behavior in Qt
		self.setSceneRect(-2000, -2000, 4000, 4000)



		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) 
		self.setVerticalScrollBarPolicy  (Qt.ScrollBarAlwaysOff)

	def mousePressEvent(self, event):
		self.treat_event(event)
		super(TreeView, self).mousePressEvent(event)
		# self.scene.update()

	def treat_event(self, event):
		""" "treat_event" can be replaced programmatically to implement custom mouse behavior """
		pass


	def reload(self):
		self.scene.update()

class TreeScene(QGraphicsScene):
	"""docstring for TreeScene"""
	def __init__(self, *args, **kwargs):
		super(TreeScene, self).__init__(*args, **kwargs)
		self.tree_obj = TreeObject(None)
		self.addItem(self.tree_obj)
		self.setBackgroundBrush(
			QBrush(
				QColor(
					*cst.style["background"]["color"]
				)
			)
		)
		# self.addItem(Handle())

