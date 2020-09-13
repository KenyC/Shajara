from PyQt5.QtCore    import Qt
from PyQt5.QtWidgets import QApplication


import utils
import cst



class ViewMouseManager:
	"""Manages click, drag event on the tree graphics view"""

	sprout_dist = cst.style["nodes"]["sensitivity"]

	def __init__(self, view, synchronizer):
		self.view         = view
		self.synchronizer = synchronizer
		self.tree         = self.synchronizer.tree
		
		self.view.treat_event = self.effect

	def effect(self, event):
		self.add_remove_node(
			self.view.mapToScene(event.pos()),
			event.buttons()
		)

	def add_remove_node(self, scene_pos, buttons):
		for i, p in enumerate(self.tree.positions):
			if utils.dist((scene_pos.x(), scene_pos.y()), p) < ViewMouseManager.sprout_dist:
				modifiers = QApplication.keyboardModifiers()

				if cst.behavior["view"]["select_node"](buttons, modifiers):
					self.synchronizer.select_node(i)
				elif cst.behavior["view"]["add_node"]     (buttons, modifiers):
					self.tree.sprout(i)
					self.synchronizer.update_tree()
				elif cst.behavior["view"]["remove_node"](buttons, modifiers):
					self.tree.delete(i)
					self.synchronizer.update_tree()

				return
