from .transducer import Transducer
from tree import Tree

# %%
from tree.transducer import Transducer
from tree import Tree

# %%

DEFAULT_BLANK_QTREE = "\t"


class QTreeTrans(Transducer):
	""" Daughter class for QTree representation """

	def toUnsat(tree, labels):
		
		def toUnsatRec(tree, idx, space):
			if not tree.children[idx]:
				return [space*DEFAULT_BLANK_QTREE + "{", labels[idx], "} \n"]
			else:
				returnStr = []
				returnStr.append(space*DEFAULT_BLANK_QTREE + "[.{")
				returnStr.append(labels[idx])
				returnStr.append("} \n")

				for c in tree.children[idx]:
					returnStr += toUnsatRec(tree, c, space + 1)
				
				returnStr.append(space*DEFAULT_BLANK_QTREE + "]\n")
				return returnStr

		return ["\\Tree ","\n"] + toUnsatRec(tree, 0, 0)

	def parse(string):

		
		stack = []
		countBracket = 0
		lastTree = None

		for c in string:



			if c == "}":
				# collapse literals till "{"

				topChar = ""
				while stack[-1] != "{":
					stack[-1] += topChar
					topChar = stack.pop()

				stack.pop() 
				stack.append("{" + topChar + "}")
				countBracket -= 1

			elif c == "]" and countBracket == 0:
				elemTrees = []


				while len(elemTrees) != 3:
					topElem = stack.pop()

					if isinstance(topElem, Tree):
						elemTrees.append(topElem)
					elif topElem[0] == "{" and topElem[-1] == "}":
						elemTrees.append(Tree(label = topElem[1:-1]))

				topElem = ""
				while topElem != "[":
					topElem = stack.pop()

				elemTrees[2] = elemTrees[2].labels[0]
				lastTree = Tree.merge_trees(elemTrees[:-1][::-1], label = elemTrees[2])
				stack.append(lastTree)

			else:
				stack.append(c)
				if c == "{":
					countBracket += 1

		return lastTree


# %%