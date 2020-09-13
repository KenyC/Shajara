from .transducer import Transducer

DEFAULT_BLANK_HASKELL = "   "

class HaskellTrans(Transducer):
	""" Daughter class for my Haskell implementation of H&K """

	def toUnsat(tree, labels):
		def toUnsatRec(tree, idx, space):
			if not tree.children[idx]:
				return [space*DEFAULT_BLANK_HASKELL + "(", labels[idx], ")\n"]
			else:
				returnStr = []
				if idx != 0:
					returnStr.append(space*DEFAULT_BLANK_HASKELL + "(\n")

				for i,c in enumerate(tree.children[idx]):
					returnStr += toUnsatRec(tree, c, space + 1)
					if i != len(tree.children[idx]) - 1:
						returnStr.append((space + 1)*DEFAULT_BLANK_HASKELL + "  <^>\n")
				
				if idx != 0:
					returnStr.append(space*DEFAULT_BLANK_HASKELL + ")\n")
				
				return returnStr

		return toUnsatRec(tree, 0, 0)