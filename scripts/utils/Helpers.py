import lx

class UserValue(object):
    '''
    Helper Class for user values. Creates an user value with init.
    Values which are already there are not overwritten.
    '''
    
    def __init__(self, name, prefix=None, type_='string', life='temporary'):
        name = name.replace(' ', '_')
        self.name = '{%s.%s}' % (prefix, name) if prefix else str(name)
        self._create(type_=type_, life=life)
    
    def _create(self, type_='string', life='temporary'):
        '''
        Create new user value. You should not need to call this method
        '''
        try:
            lx.eval('!user.value %s ?' % self.name)
        except:
            lx.eval('user.defNew %s type:%s life:%s' % (self.name, type_, life))
        else:
            print 'A user value with %s already exists' % self.name
    
    def set(self, value):
        '''
        Set a new value
        '''
        lx.eval('user.value %s %s' % (self.name, value))
    
    @property
    def value(self):
        '''
        Get current value
        '''
        return lx.eval('user.value %s ?' % self.name)