import cst



class TransducerManager:
	"""Manages changes to the combo box transducers"""

	def __init__(self, combo_box, synchronizer):
		self.combo_box = combo_box
		self.synchronizer = synchronizer
		
		self.combo_box.currentIndexChanged.connect(self.effect)	

	def effect(self, index):
		self.synchronizer.transducer = cst.transducers[index][1]
		self.synchronizer.update_text()