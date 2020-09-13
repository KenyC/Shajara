from PyQt5.QtWidgets import QTextEdit, QApplication
from PyQt5.QtCore    import Qt

class ValidateText(QTextEdit):
	"""Makes Enter key board press copy to clipboard"""


	def keyPressEvent(self, event):
		if self.treat_event(event):
			return
		elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Return: 
			QApplication.clipboard().setText(self.toPlainText())
		else:
			super(ValidateText, self).keyPressEvent(event)

	def treat_event(self, event):
		return False

