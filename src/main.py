import sys

from PyQt5 import QtWidgets

from tree       import Tree
import tree.transducer as transducer
import ui
import events
import cst

__version__ = "1.0"

class TreeGuiApp(QtWidgets.QMainWindow, ui.Ui_MainWindow):


	def __init__(self):
		
		# Setting up window
		super(TreeGuiApp, self).__init__()
		self.setupUi(self)
		
		for name, _ in cst.transducers:
			self.transducers.addItem(name)

		self.status_bar.addWidget(QtWidgets.QLabel(cst.help_message))

		self.initialize_tree()
		self.tree_view.scene.tree_obj.tree = self.tree

		# Event managers
		self.synchronizer = events.SyncTree(self.tree_view, self.tree_repr, self.tree, transducer.QTreeTrans)
		self.synchronizer.update_tree()

		self.text_change_mgr = events.TextManager (self.tree_repr, self.status_bar, self.synchronizer) 
		self.view_mouse_mgr  = events.ViewMouseManager  (self.tree_view,   self.synchronizer)
		self.transducers_mgr = events.TransducerManager (self.transducers, self.synchronizer)
		self.clear_mgr       = events.Clear             (self.clear,       self.status_bar, self.synchronizer)
		self.import_mgr      = events.Import            (self.from_clip,   self.status_bar, self.synchronizer)


	def initialize_tree(self):
		""" 
		Initial tree looks like this:
		        /\
		         /\
		          /\
		"""
		self.tree = Tree()
		self.tree.sprout(0)
		self.tree.sprout(2)
		self.tree.sprout(4)
		self.tree.sprout(6)

		# self.tree.construct((-200, -350))
		# print(self.tree.positions)





	


 
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = TreeGuiApp()
	# assert(False)
	window.show()
	sys.exit(app.exec_())