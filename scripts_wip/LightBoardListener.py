import lxifc
import lx
import modo


class LightListener(lxifc.SceneItemListener):
    """Listener for """
    
    undoService = lx.service.Undo()
    
    def __init__(self):
        """
        Create new listener server
        """
        self.listenerService = lx.service.Listener()
        self.COM_object = lx.object.Unknown(self) # unkown COM object?
        self.listenerService.AddListener(self.COM_object)
    
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
            lx.out('New Light: ',item.Ident())
            
    def sil_ItemRemove(self, item):
        
        # Bail out if there is no undo context. Must be checked
        if not LightListener.undoService.State() == lx.symbol.iUNDO_ACTIVE:
            return        
        
        item = lx.object.Item(item)
        if item.TestType(modo.constants.LIGHT_TYPE):
            lx.out('Deleted Light: ', item.Ident())        


class LightSelectionListener(lxifc.SelectionListener):
    """
    SelectionListener for lights
    """
    
    undoService = lx.service.Undo()
        
    def __init__(self):
        """
        Create new listener server
        """
        self.listenerService = lx.service.Listener()
        self.listenerService.AddListener(self)
    
    def __del__(self):
        """
        Kill the listener server
        """
        self.listenerService.RemoveListener(self)
    
    def selevent_Add(self, type, subtType):
        SceneService = lx.service.Scene()
        type_id = SceneService.ItemTypeSuper(subtType)
        if modo.constants.LIGHT_TYPE == type_id:
            scene = modo.Scene()
            selected = scene.selectedByType(subtType)[0]
            lx.out('Selected Light: %s' % selected.id)
    
    def selevent_Current(self, type):
        pass
    
    def selevent_Remove(self, type, subtType):
        pass
    
    def selevent_Time(self, time):
        pass
    
    def selevent_TimeRange(self, type):
        pass
        
LightListener = LightListener()
LightSelectionListener = LightSelectionListener()