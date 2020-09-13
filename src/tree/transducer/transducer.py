import re

from tree import Tree
import utils

# HELPER FUNCTIONS
def escapeBraces(str):
	return str.replace("\\", "\\\\").replace("{",r"\{").replace("}",r"\}").replace("[",r"\[").replace("]",r"\]").replace("^","\^").replace("(","\(").replace(")","\)").replace("+","\+")


	
class Transducer:
	"""
	Abstract class for tree-to-string transducer

	Methods:
		- toUnsat : returns the structure of the tree in list of strings format formattable blanks, where the labels should be inserted (to be overloaded by daughter classes)
		- toStr : returns the string representation of the tree with its labels
		- regExp : compiles a regular expression that matches the tree's structure to strings ; 
		  this regular expression, in combination with indicesOrder, allows recovery of tree labels from string
		- indicesOrder : returns a look-up list where the i-th value is the index of the node at that position.
	"""

	def toUnsat(tree, labels):
		""" return expressions with list of strings with labels in place """
		return labels
	
	@classmethod
	def toStr(cls, tree):
		return "".join(cls.toUnsat(tree, tree.labels))


	@classmethod
	def regExp(cls, tree):
		""" Create a list with blanks where labels should be """
		blankList = cls.toUnsat(tree, ["" for i in range(tree.n)])
		regexp = ["(.*)" if s == "" else escapeBraces(s) for s in blankList]
		#regexp = escapeBraces(cls.toUnsat(tree).format(*["(.*)" for i in range(tree.n)]))
		return re.compile("".join(regexp))

	@classmethod
	def indicesOrder(cls, tree):
		return list(filter(lambda x: isinstance(x, int), cls.toUnsat(tree, range(tree.n))))

	@classmethod
	def find(cls, tree, i):
		listStr = cls.toUnsat(tree, range(tree.n))
		index = next( (j for j,x in enumerate(listStr) if isinstance(x, int) and x == i), -1)
		fillLabel = [tree.labels[word] if isinstance(word, int) else word for word in listStr]
		beginning = len("".join(fillLabel[:index]))
		return {"start": beginning, "end": beginning + len(tree.labels[i])}




if __name__ == "__main__":
	string = r"""
	\Tree
	[.{fezfe}
	[.{efz} {efz} {ezfe}]
	[.{zfeef} {efzef}  [.{fez} {zefef} {ezfef} ]]
	]
	"""

	# Test values for debugging
	testTree = Tree()
	testTree.sprout(0)
	testTree.sprout(1)
	testTree.sprout(2)
	testTree.sprout(4)
	testTree.sprout(6)

	testTree2 = testTree.copy()
	testTree2.labels = ["efz","ezfefz","joi","ohiho","trl","cvj","gjph","trb","erb","reh","gzr"]

	testString = "\\Tree \n[.{aab} \n\t[.{efzfe} \n\t\t{zddz} \n\t\t[.{4zddz} \n\t\t\t{7dzdz} \n\t\t\t{dzdz8zdzd} \n\t\t]\n\t]\n\t[.{zazd2dzzd} \n\t\t{dzzd5zddz} \n\t\t[.{dd6ddzzd} \n\t\t\t{dzdz9dzzd} \n\t\t\t{dzdz10zdz} \n\t\t]\n\t]\n]\n"
	testString2 = "\\Tree \n[.{} \n\t[.{} \n\t\t{} \n\t\t[.{} \n\t\t\t{} \n\t\t\t{} \n\t\t]\n\t]\n\t[.{} \n\t\t{} \n\t\t[.{} \n\t\t\t{} \n\t\t\t{} \n\t\t]\n\t]\n]\n"
