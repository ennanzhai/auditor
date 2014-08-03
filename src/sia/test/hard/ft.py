'''
This file aims to define the class of nodes in fault tree

'''
global pathID
pathID = "0"

class TreeNode:
    def __init__(self):
        self.ID = ""
        self.childList = []
        self.gate = "AND"
        self.traverse = 0
        self.happen = 0
        self.parentList = []
        self.childHappenList = []
        self.alreadySigned = 0

