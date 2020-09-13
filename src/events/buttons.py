from PyQt5.QtWidgets import QApplication

import cst

class ButtonManager:
	""" Managing effects of button """
	def __init__(self, button, status_bar, synchronizer):
		super(ButtonManager, self).__init__()
		self.button = button
		self.synchronizer = synchronizer
		self.tree         = self.synchronizer.tree
		self.status_bar = status_bar

		self.button.clicked.connect(self.effect)

	def effect(self):
		pass


class Clear(ButtonManager):
	""" Strips Labels from tree"""
	def effect(self):
		self.tree.labels = ["" for _ in range(self.tree.n)]
		self.synchronizer.update_tree()


class Import(ButtonManager):
	""" Imports tree from clipboard """
	def effect(self):
		content_clipboard = QApplication.clipboard().text()

		try:
			new_tree = self.synchronizer.transducer.parse(content_clipboard)
		except Exception as e:
			self.status_bar.showMessage("Parse not implemented for this transducer", cst.message_timeout)
			return 

		if new_tree is not None:
			self.synchronizer.tree.set(new_tree)
			self.synchronizer.update_tree()
		else:
			self.status_bar.showMessage("Could not parse tree in clipboard", cst.message_timeout)

