#python

import modo
import lx
from collections import namedtuple

from utils.Helpers import UserValue

scene = modo.Scene()
renderItem = scene.items(itype=lx.symbol.sITYPE_RENDER)[0]

def get_backdrop(camera):
    for clip in scene.items(itype = lx.symbol.sITYPE_VIDEOSEQUENCE):
        # todo: what if more than one camera has that clip assigned?
        for cam in clip.itemGraph('shadeLoc').reverse():
            if cam == camera:
                file_path = clip.channel('pattern').get()
                first_fame = clip.channel(lx.symbol.sICHAN_VIDEOSEQUENCE_FIRSTFRAME).get()
                last_frame = clip.channel(lx.symbol.sICHAN_VIDEOSEQUENCE_LASTFRAME).get()        
    
                return {'range':(first_fame, last_frame), 'filePath':file_path, 'clipObj':clip}
        else:
            return None

def get_render_cam(renderItem):
    return renderItem.itemGraph('shadeLoc').forward(0)

# Modo commands
def set_range_from_clip():
    clip = get_backdrop(get_render_cam(renderItem))
    if clip:
        scene.sceneRange = clip['range']
        renderItem.channel(lx.symbol.sICHAN_POLYRENDER_FIRST).set(clip['range'][0])
        renderItem.channel(lx.symbol.sICHAN_POLYRENDER_LAST).set(clip['range'][1])

def disable_backdrop(camera):
    """
    Save the current backdrop id to a unique user value and
    then remove it from the camera
    """
        
    camUserVal = UserValue(camera.name, prefix='PlateManager')
    current_backdrop = camUserVal.value
    
    try:
        backdrop = camera.itemGraph('shadeLoc').forward(0)
    except:
        backdrop = None
    else:
        # Save the backdrop id to the user value
        if current_backdrop != backdrop.id:
            camUserVal.set(backdrop.id)
        
        # remove the back drop from the camera
        backdrop.itemGraph('shadeLoc').disconnectInput(camera)

def enable_backdrop(camera):
    """
    Enable the last assigned backdrop for a camera
    """
    
    camUserVal = UserValue(camera.name, prefix='PlateManager')
    backdrop_id = camUserVal.value
    try:
        backdrop = modo.Item(backdrop_id)
    except LookupError as e:
        print 'No Backdrop found with id: %s' % backdrop_id
    else:
        backdrop.itemGraph('shadeLoc').connectInput(camera)
    
# Commands
arg = lx.args()[0]
if arg == 'setRange':
    set_range_from_clip()
    
if arg == 'disableBackdrop':
    selected_cameras = scene.selectedByType(modo.c.CAMERA_TYPE)
    if len(selected_cameras) == 0:
        modo.dialogs.alert('Plate Manager', 'Please select one or more cameras')
    else:
        for camera in selected_cameras:
            disable_backdrop(camera)

if arg == 'enableBackdrop':
    selected_cameras = scene.selectedByType(modo.c.CAMERA_TYPE)
    if len(selected_cameras) == 0:
        modo.dialogs.alert('Plate Manager', 'Please select one or more cameras')
    else:
        for camera in selected_cameras:
            enable_backdrop(camera)