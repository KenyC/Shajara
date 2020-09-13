from PyQt5.QtCore      import Qt
from PyQt5.QtWidgets import QApplication

import cst 

class TextManager(object):
	"""Event manager for any changes in input field """
	def __init__(self, field, status_bar, synchronizer):
		self.field = field
		self.status_bar = status_bar
		self.synchronizer = synchronizer
		self.tree = self.synchronizer.tree
		self.field.textChanged.connect(self.redraw)
		self.field.treat_event = self.change_node

	

	def redraw(self):
		match = self.synchronizer.str_tree_regex.match(self.field.toPlainText())

		if match is not None:
			for text_pos, label in enumerate(match.groups()):
				self.tree.labels[self.synchronizer.text_pos_to_tree_pos[text_pos]] = label

			self.synchronizer.update_view()
		else:
			# Out of sync
			# display error message
			self.status_bar.showMessage("Shape of tree in text field and view do not match. Only changes to view will be taken into account.", cst.message_timeout)
			pass


	def change_node(self, event):
		if event.key() == Qt.Key_Tab:

			if QApplication.keyboardModifiers() & Qt.ControlModifier:
				move_to = self.tree.previous_reverse_polish
			else:
				move_to = self.tree.next_reverse_polish
			

			text_position = self.field.textCursor().position()
			match = self.synchronizer.str_tree_regex.match(self.field.toPlainText())

			if match is not None:

				for i in range(1, match.lastindex + 1):

					if text_position < match.start(i):
						return False
					elif match.start(i) <= text_position <= match.end(i):
						# Cursor is in a node!
						print(self.tree.children)
						next_node = move_to(self.synchronizer.text_pos_to_tree_pos[i - 1])
						self.synchronizer.select_node(next_node)
						return True

		return False
		