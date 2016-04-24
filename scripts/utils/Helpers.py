try:
    import lx
except ImportError:
    pass


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
    Resize an image sequence. Supported output image formats are EXR, TGA, PNG, JPG
    
    The image conversion is done with oiiotool
    
    :param image_path: modo image file path
    :type image_path: str
    :param size: Resize factor in percent
    :type size: int
    :param force: If true writes files into existing output directory and overwrite existing files
    :type force: bool
    :return: target directory
    :rtype: str
    '''
    
    from subprocess import Popen
    from os import path
    from os import makedirs
    import shutil
    import time
    import sys
    
    # Absolute file path of Lightbox
    FileService = lx.service.File()
    oiiotool = FileService.ToLocalAlias('kit_LightBox:')
    oiiotool = path.join(oiiotool, 'scripts', 'utils', 'oiiotool')
    
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
            
    cmd = [oiiotool, path.join(dir_, name), '--resize', '%s%%' % size, '-o', path.join(target_dir, export_name)]
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
    
    process = Popen(cmd)
    process.communicate()
    
    print 'Proxys created: %s' % path.join(target_dir, export_name)
    return target_dir

def create_video(file_path):
    """
    -f image2 -i "/Users/bjoern_siegert/Projects_local/TrollBridge/shots/TB_00610/render/v01/TB_00610_lighting_v01_Final Color Output%*.png" -crf 5 -c:v h264 -r 25 -vf scale=1280:-2 -pix_fmt yuv420p test.mov
    """
    
    import os
    import subprocess
    
    # Absolute file path of Lightbox
    try:
        FileService = lx.service.File()
    except:
        ffmpegtool = './ffmpeg'
    else:
        ffmpegtool = FileService.ToLocalAlias('kit_LightBox:')
        ffmpegtool = os.path.join(ffmpegtool, 'scripts', 'utils', 'ffmpeg')    
    
    # create output file name
    # we need remove the wildcard and change the file format
    fn = os.path.basename(file_path)
    fn = fn.replace('%*', '')
    fn = os.path.splitext(fn)[0] + '.mov'
    # the output dir is one level up of the source
    output_dir = os.path.dirname(os.path.dirname(file_path))
    
    fn = os.path.join(output_dir, fn)
    
    cmd = [ffmpegtool, '-f', 'image2',
           '-i', '%s' % file_path, 
           '-crf', '5', 
           '-c:v', 'h264', 
           '-r', '25', 
           '-vf', 'scale=1280:-2',
           '-pix_fmt', 'yuv420p',
           '%s' % fn]
    log = subprocess.check_output(cmd)
    print log

def _find_files(file_path, wildcard='%*'):
    """
    Find frame pattern in files in a given file path. The number pattern gets replaced and can be specified.
    
    :param file_path: file path
    :param wildcard: wildcard which replaces the number pattern in the files
    :type file_path: string
    :type wildcard: string
    :return: file paths
    :rtype: list
    """
    
    import re
    import os
    
    data = []
    for fn in os.listdir(file_path):
        find = re.search('(.*?)(\d+)\.', fn)
        try:
            pattern = find.groups()[1]
        except:
            continue
        else:
            fn_new = fn.replace(pattern, wildcard)
            fn_new = os.path.join(file_path, fn_new)
            if fn_new not in data:
                data.append(fn_new)
    
    return data
        

if __name__ == '__main__':
    # quick test
    #f = '/Users/bjoern_siegert/Projects_local/TrollBridge/shots/TB_00610/plate/TB_00610_Plate_TGA_UNDISTORTED/TB_00610_#.tga'
    #create_proxy(f, force=True, file_type='JPG')
    f = '/Users/bjoern_siegert/Projects_local/TrollBridge/shots/TB_00830/render/v02/TB_00830_lighting_v02_Final Color Output%*.png'
    create_video(f)
