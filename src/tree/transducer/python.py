from .transducer import Transducer

DEFAULT_BLANK_PYTHON = "\t"


class PythonTrans(Transducer):
	""" Daughter class for my Python implementation of H&K """

	def toUnsat(tree, labels):
		def toUnsatRec(tree, idx, space):
			if not tree.children[idx]:
				return [space*DEFAULT_BLANK_PYTHON + "(", labels[idx], ")"]
			else:
				returnStr = []
				if idx != 0:
					returnStr.append(space*DEFAULT_BLANK_PYTHON + "(\n")

				for i,c in enumerate(tree.children[idx]):
					returnStr += toUnsatRec(tree, c, space + 1)
					if i != len(tree.children[idx]) - 1:
						returnStr.append("  +\\\n")
					else:
						returnStr.append("  \n")
				
				if idx != 0:
					returnStr.append(space*DEFAULT_BLANK_PYTHON + ")")
				
				return returnStr

		return toUnsatRec(tree, 0, -1)