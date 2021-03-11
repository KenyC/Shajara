from PyQt5.QtGui     import QTextCursor

ROOT_POS    = (-200, -350)

class SyncTree:

	def __init__(self, view, text, tree, transducer):
		self.view = view
		self.text = text

		self.tree       = tree
		self.transducer = transducer

	def update_tree(self):
		""" Redraws tree & change text edit"""
		self.update_view()
		self.update_text()

	def update_text(self):
		""" Change text edit view and updates pattern """
		self.str_tree_regex       = self.transducer.regExp      (self.tree)
		self.text_pos_to_tree_pos = self.transducer.indicesOrder(self.tree)
		self.update_labels()

	def update_labels(self):
		""" Change text edit view """

		# To avoid firing textChanged, we temporarily block signals from the text editor
		self.text.blockSignals(True)
		self.text.setText(self.transducer.toStr(self.tree))
		self.text.blockSignals(False)

	def update_view(self):
		""" Redraws tree """
		self.tree.compute_display_positions(ROOT_POS)
		self.view.scene.update()

	def select_node(self, node_idx):
		self.text.setFocus()

		positions = self.transducer.find(self.tree, node_idx)
		cursor = self.text.textCursor()
		cursor.setPosition(positions["end"])
		cursor.setPosition(positions["start"], QTextCursor.KeepAnchor)
		self.text.setTextCursor(cursor)
