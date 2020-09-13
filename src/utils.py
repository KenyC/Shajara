import re

# Euclidian distance between two pairs
def dist(p1, p2):
	return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5


js_comments = re.compile(r"(//[^\n]*\n)|(\/\*[^\/]*\*\/)")

def strip_js_comments(string):
	""" Strips js comments from json file """
	return js_comments.sub("", string)
