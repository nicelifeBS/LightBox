import lxifc
import lx
import modo


class TreeNode(object):

    _Primary = None

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.columns = (('Lights', -1), ) # if you want one column it needs to be a two sized tuple
        self.selected = False

    def add_node(self, name):
        self.children.append(TreeNode(name, self))
        return self.children[-1]

    def remove_node(self, name):
        for n in self.children:
            if n.name == name:
                self.children.remove(n)

    def is_selected(self):
        return self.selected

    def set_selected(self, val=True):
        if val:
            self.setPrimary(self)
        self.selected = val

    def clear_selection(self):
        if self._Primary:
            self.setPrimary()

        self.set_selected(False)

        for child in self.children:
            child.clear_selection()

    @classmethod
    def setPrimary(cls, primary=None):
        cls._Primary = primary

    @classmethod
    def getPrimary(cls):
        return cls._Primary

tree_root = TreeNode('Lights')
#tree_root.add_node('test')

ITEM_ADD = 0
ITEM_DELETE = 1

class LightListener(lxifc.SceneItemListener):
    """Listener for """

    undoService = lx.service.Undo()

    def __init__(self, callback):
        """
        Create new listener server
        """
        self.listenerService = lx.service.Listener()
        self.callback = callback
        self.item = None
        self.event = None

    def __del__(self):
        """
        Kill the listener server
        """
        self.listenerService.RemoveListener(self.COM_object)

    def sil_ItemAdd(self, item):
        """
        Get newly created items
        """

        # Bail out if there is no undo context. Must be checked
        if not LightListener.undoService.State() == lx.symbol.iUNDO_ACTIVE:
            return

        item = lx.object.Item(item)
        if item.TestType(modo.constants.LIGHT_TYPE):
            self.item = item.Ident()
            self.event = ITEM_ADD
            self.callback(self)

    def sil_ItemRemove(self, item):

        # Bail out if there is no undo context. Must be checked
        if not LightListener.undoService.State() == lx.symbol.iUNDO_ACTIVE:
            return

        item = lx.object.Item(item)
        if item.TestType(modo.constants.LIGHT_TYPE):
            self.item = item.Ident()
            self.event = ITEM_DELETE
            self.callback(self)


class LightBrowser(lxifc.TreeView, lxifc.Tree, lxifc.Attributes, lxifc.ListenerPort):

    # Gloabal list of all created tree views.
    # These are used for shape and attribute changes
    _listenerClients = {}

    def __del__(self):
        """Clean up the listener"""
        lx.service.Listener().RemoveListener(self.COM_object)

    def __init__(self, node=None, index=0):
        if node:
            self.current_node = node
        else:
            self.current_node = tree_root

            self.item_events = LightListener(self.item_event_callback)
            self.COM_object = lx.object.Unknown(self.item_events)
            lx.service.Listener().AddListener(self.COM_object)

        self.current_index = index

    # Listender port
    @classmethod
    def addListenerClient(cls, listener):
        """
        Whenever a new tree view is created, we will add
        a copy of its listener so that it can be notified
        of attribute or shape changes
        """
        treeListenerObj = lx.object.TreeListener(listener)
        cls._listenerClients[treeListenerObj.__peekobj__()] = treeListenerObj

    @classmethod
    def removeListenerClient(cls, listener):
        """
        When a view is destroyed, it will be removed from
        the list of clients that need notification.
        """
        treeListenerObject = lx.object.TreeListener(listener)
        if cls._listenerClients.has_key(treeListenerObject.__peekobj__()):
            del cls._listenerClients[treeListenerObject.__peekobj__()]

    @classmethod
    def notify_NewShape(cls):
        for client in cls._listenerClients.values():
            if client.test():
                client.NewShape()

    @classmethod
    def notify_NewAttributes(cls):
        for client in cls._listenerClients.values():
            lx.out(client)
            if client.test():
                client.NewAttributes()

    def lport_AddListener(self, obj):
        """
        Called from core code with the object that wants to
        bind to the listener port
        """
        self.addListenerClient(obj)

    def lport_RemoveListener(self, obj):
        """
        Called from core when a listener needs to be removed from
        the port.
        """
        self.removeListenerClient(obj)

    def item_event_callback(self, listener):
        """
        Here we handle different events from our light listener.
        E.g. add new lights or remove deleted lights
        :param listener: light listener object
        :return:
        """
        if listener:
            if listener.event == ITEM_ADD:
                tree_root.add_node(str(listener.item))
                self.notify_NewShape()
            if listener.event == ITEM_DELETE:
                tree_root.remove_node(str(listener.item))
                self.notify_NewShape()

    def target_node(self):
        """Current targeted node in the current tier"""
        return self.current_node.children[self.current_index]

    def tree_Spawn(self, mode):
        new_tree = LightBrowser(self.current_node, self.current_index)
        new_tree_obj = lx.object.Tree(new_tree)

        # if mode == lx.symbol.iTREE_PARENT:
        #     # move the tree to the parent tier
        #     new_tree_obj.ToParent()
        #
        # elif mode == lx.symbol.iTREE_CHILD:
        #     # move tree to child tier
        #     new_tree_obj.ToChild()
        #
        # elif mode == lx.symbol.iTREE_ROOT:
        #     # move tree to root tier
        #     new_tree_obj.ToRoot()

        return new_tree_obj

    def tree_ToParent(self):
        """Step up to parent tier and set selection in this tier to the current index"""
        parent = self.current_node.parent
        if parent:
            self.current_index = parent.children.index(self.current_node)
            self.current_node = parent

    def tree_ToChild(self):
        """Set current node to child of node"""
        self.current_node = self.current_node.children[self.current_index]

    def tree_ToRoot(self):
        """Move back to the root"""
        self.current_node = tree_root

    def tree_IsRoot(self):
        """Is current tier root?"""
        if self.current_node == tree_root:
            return True
        else:
            return False

    def tree_ChildIsLeaf(self):
        """If current tier has no children then it is considered a leaf"""
        if len(self.current_node.children) > 0:
            return False
        else:
            return True

    def tree_Count(self):
        """Number of nodes in tier"""
        return len(self.current_node.children)

    def tree_Current(self):
        """Retrun the current index of the targeted item"""
        return self.current_index

    def tree_SetCurrent(self, index):
        self.current_index = index


    #----------------------
    # TreeView
    #----------------------

    # Set up the columns we need for our tree
    def treeview_ColumnCount(self):
        return len(tree_root.columns)

    def treeview_ColumnByIndex(self, columnIndex):
        return tree_root.columns[columnIndex]

    # def treeview_ToPrimary(self):
    #     """Move the tree to the primary selection"""
    #     if self.current_node._Primary:
    #         self.current_node = self.current_node._Primary
    #         self.tree_ToParent()
    #         return True
    #     else:
    #         return False

    # Is node selected in tree view
    def treeview_IsSelected(self):
        return self.target_node().is_selected()

    # Selection handling in view
    def treeview_Select(self, mode):
        if mode == lx.symbol.iTREEVIEW_SELECT_PRIMARY:
            tree_root.clear_selection()
            self.target_node().set_selected()
        # elif mode == lx.symbol.iTREEVIEW_SELECT_ADD:
        #     self.target_node().set_selected()
        # elif mode == lx.symbol.iTREEVIEW_SELECT_REMOVE:
        #     self.target_node().set_selected(False)
        elif mode == lx.symbol.iTREEVIEW_SELECT_CLEAR:
            tree_root.clear_selection()

    # Attributes to retrieve the name of the node
    # to populate the tree view
    def attr_Count(self):
        return len(tree_root.columns)

    def attr_GetString(self, index):
        node = self.current_node.children[self.current_index]
        if index == 0:
            return node.name
        else:
            return ''


tags = {lx.symbol.sSRV_USERNAME: "lightbrowser",
        # register the view type: Class of viewport, four characters for identifier, alternative string as identifier, Name in viewport dropdown
        lx.symbol.sTREEVIEW_TYPE: "vpapplication LBTV lightbrowser LightBrowser"}

lx.bless(LightBrowser, 'LightBrowser', tags)