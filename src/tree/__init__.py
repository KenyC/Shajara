
class Tree:
	"""
	Trees are stored in a flat representation 

	Attributes:
		- children (list[list[int]): index i, self.children[i] is the set of indices that are children to i
		- labels   (list[str])     : label of nodes

	IMPORTANT
	Always make sure that children always come after fathers
	"""



	def __init__(self, label = "", children = None):
		self.labels = [label]
		if children is None:
			self.children = [[]]
		else:
			self.children = children

	def merge_trees(children, label = ""):
		sums = [1]

		for child in children[:-1]:
			sums.append(sums[-1] + child.n)

		nodes = [[subnode + increment for subnode in node] for increment, child in zip(sums, children) for node in child.children]
		labels = sum([child.labels for child in children], [label])

		t = Tree() 		
		t.children = [sums] + nodes
		t.labels = labels

		return t

	def sprout(self, idx, labelL = "", labelR = ""):
		""" Add two children to a leaf or adds a parent to an internal node, labels optional """

		if not self.children[idx]:
			self.labels        += [labelL, labelR]
			self.children[idx] += [self.n , self.n + 1]
			self.children      += [[],[]]
		else:
			iFather = self.father(idx)
			

			self.insert_child(idx, labelR, [idx])

			if iFather is not None:
				self.children[iFather] = [idx if x == idx + 1 else x for x in self.children[iFather]]

			self.labels.append(labelL)
			self.children.append([])

			self.children[idx] = [self.n - 1] + self.children[idx]
	
	def father(self, idx):
		return (next( (j for j, child in enumerate(self.children) if idx in child), None))

	def insert_child(self, idx, label = "", children = None):
		lookUpFun = lambda i: i if i < idx else (i + 1)

		if children is None:
			ch = []
		else:
			ch = list(map(lookUpFun, children))

		self.children = [list(map(lookUpFun, child)) for child in self.children]
		self.children.insert(idx, ch)
		self.labels.insert(idx, label)

	def make_reverse_polish(self, node = 0):
		for child in self.children[node]:
			for element in self.make_reverse_polish(child):
				yield element
		yield node


	def next_reverse_polish(self, node):
		""" Returns the node to the right of "node" when tree is linearized in reverse Polish notation """
		polish_sequence = list(self.make_reverse_polish())
		position = polish_sequence.index(node)
		return polish_sequence[(position + 1) % self.n]


	def previous_reverse_polish(self, node):
		""" Returns the node to the right of "node" when tree is linearized in reverse Polish notation """
		polish_sequence = list(self.make_reverse_polish())
		position = polish_sequence.index(node)
		return polish_sequence[(position - 1) % self.n]


	@property
	def n(self):
		return len(self.children)
	
	def delete(self, idx):
		""" Delete all children of node idx """

		self.children[idx] = []
		# Some nodes may no longer be connected to the root ; delete them
		self.trim()

	def accessible(self, idx = 0):
		""" Returns the list of descendants of node "idx" ("idx" included) """
		l = [idx]
		for j in self.children[idx]:
			l.extend(self.accessible(j))

		return l

	def leaves(self, node = 0):
		if self.children[node]:
			for child in self.children:
				for leaf in self.leaves(child):
					yield leaf
		else:
			yield node

	def trim(self):
		""" Remove nodes that are inaccessible from the root """

		acc = self.accessible()

		# Stores the new position of nodes as function of the old position
		invAcc = {idx:i for i,idx in enumerate(acc)}

		# Creates new labels and children list from only the set of accessible nodes
		newLabels = [self.labels[idx] for idx in acc]
		newChildren = [self.children[idx] for idx in acc]

		# The position of nodes in the list has changed
		# Use the look-up table "invAcc" to replace old position of children with the new ones
		for i, cdren in enumerate(newChildren):
			newChildren[i] = [invAcc[c] for c in cdren]

		# Finally, update the tree with new values
		self.labels = newLabels
		self.children = newChildren

	def show(self, idx = 0, space = 0):
		""" Prints simple representation of tree in string format (for debugging purposes)"""
		print(space*" "+ (str(idx) if self.labels[idx] == "" else self.labels[idx]))
		for c in self.children[idx]:
			self.show(c, space + 1)

	def compute_display_positions(self, pos, **params):
		"""
		Computes position of nodes if root is at coordinate "pos"
		Display rules:
			- A leaf has a fixed width specified in "defaults".
			- The width of a subtree is the sum of width of his children.
			- A node's X coordinate is the average of its children's X coordinate (symmetry)
			- A node is always above its children by a height specified in "defaults".
			- Between adjacent sister nodes n1 and n2, there must be a gap of at least the width of n1 and the width of n2 (prenvents overlap)
		"""

		defaults = {"node_width": 60., "height_branch": 100., "node_widths": None, "height_branches": None}
		defaults.update(params)
		same_node_width  = defaults["node_widths"]     is None
		same_node_height = defaults["height_branches"] is None

		### FIRST PASS
		# Computes the width of all subtrees
		# Computes the position of node with respect to left of the subtree it spans (mean position of children)
		# Looping from end to beginning makes sure we get to children before their mothers
		self.lgths          = [0. for _ in self.labels]
		self.loc_in_segment = [0. for _ in self.labels]
		for i in range(self.n - 1, -1, -1):
			if not self.children[i]:
				if same_node_width:
					self.lgths[i]          = defaults["node_width"]
					self.loc_in_segment[i] = defaults["node_width"] / 2
				else:
					self.lgths[i]          = defaults["node_widths"][i]
					self.loc_in_segment[i] = defaults["node_widths"][i] / 2
			else:
				running_sum_length     = 0.
				running_sum_child_pos  = 0.

				for c in self.children[i]:
					running_sum_child_pos  += running_sum_length + self.loc_in_segment[c]
					running_sum_length     += self.lgths[c]

				n_children = len(self.children[i])
				self.lgths[i]          = running_sum_length     
				self.loc_in_segment[i] = running_sum_child_pos  / n_children


		### SECOND PASS
		# Computes node position 
		# Initialization to the position of root
		self.positions = [pos for i in range(self.n)]
		for i in range(self.n):
			if self.children[i]:
				# Current node position
				x_father, y_father = self.positions[i]

				# x_position of left edge
				left_edge = x_father - self.loc_in_segment[i]

				if same_node_height:
					height = defaults["height_branch"]
				else:
					height = defaults["height_branches"][i] + defaults["height_branch"]

				# Compute position of nodes 
				for c in self.children[i]:
					self.positions[c] = (left_edge + self.loc_in_segment[c], y_father + height)
					left_edge += self.lgths[c]


	def copy(self):
		return Tree(self.labels[:],[child[:] for child in self.children])

	def set(self, tree):
		self.children = tree.children
		self.labels = tree.labels
	



if __name__ == "__main__":
	t1 = Tree(label = "t1.0")
	t1.sprout(0, labelL = "t1.1", labelR = "t1.2")
	t1.sprout(1, labelL = "t1.3", labelR = "t1.4")

	t2 = Tree(label = "t2.0")
	t2.sprout(0, labelL = "t2.1", labelR = "t2.2")
	t2.sprout(2, labelL = "t2.3", labelR = "t2.4")