class TreeNode(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []

    def add_node(self, name):
        self.children(TreeNode(name, parent=self))



