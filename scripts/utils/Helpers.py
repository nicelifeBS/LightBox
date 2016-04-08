#import lx


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
    
    
def create_proxy(img_path, size=50, file_type=None, force=False):
    '''
    :param image_path:
    :param size:
    :param force: If true writes files into existing output directory
    '''
    
    from subprocess import Popen
    from os import path
    from os import makedirs
    import shutil
    import time
    import sys
    
    file_types = ['EXR', 'TGA', 'PNG', 'JPG']
    
    # get the root dir of the image sequence
    name = path.basename(img_path)
    dir_ = path.dirname(img_path)
    root = path.dirname(dir_)
    target_dir = path.join(root, path.basename(dir_) + '_proxy')
    
    # reformat the file name because oiio expects frame patterns with one '#'
    # and modo returns more than that
    pattern = '#'
    while pattern in name:
        pattern += '#'
    else:
        # we need to remove the last one added in the while loop
        name = name.replace(pattern[:-1], '#')
    
    # Set the file file type of exported images
    if file_type:
        if file_type in file_types:
            export_name = path.splitext(name)[0] + '.%s' % file_type.lower()
        else:
            raise TypeError('Wrong file type specified. Valid formats are: %s ' % ', '.join(file_types))
    else:
        export_name = name
            
    cmd = ['./oiiotool', path.join(dir_, name), '--resize', '%s%%' % size, '-o', path.join(target_dir, export_name)]
    print ' '.join(cmd)

    try:
        makedirs(target_dir)
    except OSError as error:
        print error
        if force:
            print 'writing files anyway!'
            pass
        else:
            return None
    
    print 'Writing proxys #',
    process = Popen(cmd)
    
    while process.poll() != 0:
        sys.stdout.write('.')
        time.sleep(1)
    else:
        print '#'
        print 'Proxys created: %s' % path.join(target_dir, export_name)
        return target_dir
    
if __name__ == '__main__':
    # quick test
    f = '/Users/bjoern_siegert/Projects_local/TrollBridge/shots/TB_00560/plate/TB_00560_Plate_TGA_UNDISTORTED/TB_00560_#.tga'
    create_proxy(f, force=True, file_type='JPG')