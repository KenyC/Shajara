from .transducer import Transducer

DEFAULT_BLANK_FOREST = "\t"

class ForestTrans(Transducer):
	""" Daughter class for 'forest' """

	def toUnsat(tree, labels):
		
		def toUnsatRec(tree, idx, space):
			if not tree.children[idx]:
				return [space*DEFAULT_BLANK_FOREST + "[", labels[idx], "] \n"]
			else:
				returnStr = []
				returnStr.append(space*DEFAULT_BLANK_FOREST + "[{")
				returnStr.append(labels[idx])
				returnStr.append("} \n")

				for c in tree.children[idx]:
					returnStr += toUnsatRec(tree, c, space + 1)
				
				returnStr.append(space*DEFAULT_BLANK_FOREST + "]\n")
				return returnStr

		return ["\\begin{forest}\n"] + toUnsatRec(tree, 0, 0) + ["\\end{forest}\n"]