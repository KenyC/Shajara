from PyQt5.QtCore import Qt
import pathlib
import json

from tree.transducer import *
import utils

transducers = [
	("QTree",   QTreeTrans),
	("Haskell", HaskellTrans),
	("Forest",  ForestTrans),
	("Python",  PythonTrans)
]

##############  STYLE   ####################""

options_folder = pathlib.Path(__file__).parent.absolute() / "options"
# options_folder = pathlib.Path("/etc/opt/shajara/")
style_folder    = options_folder / "style"
behavior_folder = options_folder / "behavior"

style_file    = "style.json"
behavior_file = "behavior.json"

with open(str(style_folder / style_file), "r") as f:
	commentless_content = utils.strip_js_comments(f.read())
	style = json.loads(commentless_content)


############### BEHAVIOR ########################

with open(str(behavior_folder / behavior_file), "r") as f:
	commentless_content = utils.strip_js_comments(f.read())
	behavior_json = json.loads(commentless_content)

modifiers_map = {
	"ctrl"  : Qt.ControlModifier,
	"shift" : Qt.ShiftModifier,
	"alt"   : Qt.AltModifier,
}
mouse = {
	"left"   : Qt.LeftButton,
	"middle" : Qt.MiddleButton,
	"right"  : Qt.RightButton
}

behavior = {
	"view" : {},
	"text" : behavior_json["text"]
}

for key, val in behavior_json["view"].items():
	# The optional parameter makes the value to parameters not bound to the value of "val"
	if isinstance(val, str):
		behavior["view"][key] = lambda buttons, modifiers, val = val: bool(buttons & mouse[val]) and not bool(modifiers)
	elif len(val) == 1:
		behavior["view"][key] = lambda buttons, modifiers, val = val: bool(buttons & mouse[val[0]]) and not bool(modifiers)
	elif len(val) == 2:
		behavior["view"][key] = lambda buttons, modifiers, val = val: bool(buttons & mouse[val[1]]) and bool(modifiers & modifiers_map[val[0]])
	else:
		raise Exception("Couldn't load option files")



####################################################


help_message = " / ".join([
	"Left Clk: add two daughters",
	"Right Clk : remove descendants",
	"Ctrl+Left Clk: select node label",
	"Middle Clk: drag display",
	"Wheel: zoom "
]) 

message_timeout = 2000 # ms