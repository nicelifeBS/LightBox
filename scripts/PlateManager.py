#python

from collections import namedtuple
from utils.Helpers import UserValue
from utils.Helpers import create_proxy, _find_files, create_video

# modo
import modo
import lx


# Global objects
scene = modo.Scene()
renderItem = scene.items(itype=lx.symbol.sITYPE_RENDER)[0]
filename = scene.filename # scene file path

def get_backdrop(camera):
    for clip in scene.items(itype = lx.symbol.sITYPE_VIDEOSEQUENCE):
        for cam in clip.itemGraph('shadeLoc').reverse():
            if cam == camera:
                lx.out('Camera: %s' % cam.name)
                file_path = clip.channel('pattern').get()
                first_fame = clip.channel(lx.symbol.sICHAN_VIDEOSEQUENCE_FIRSTFRAME).get()
                last_frame = clip.channel(lx.symbol.sICHAN_VIDEOSEQUENCE_LASTFRAME).get()        
                return {'range':(first_fame, last_frame), 'filePath':file_path, 'clipObj':clip}
        
# Modo commands
def set_range_from_clip(renderItem):
    clip = get_backdrop(scene.renderCamera)
    if clip:
        scene.sceneRange = clip['range']
        scene.currentRange = clip['range']
        lx.out('frame range: %s - %s' % clip['range'])
        renderItem.channel(lx.symbol.sICHAN_POLYRENDER_FIRST).set(clip['range'][0])
        renderItem.channel(lx.symbol.sICHAN_POLYRENDER_LAST).set(clip['range'][1])

def disable_backdrop(camera):
    """
    Save the current backdrop id to a unique user value and
    then remove it from the camera
    """
        
    camUserVal = UserValue(camera.id, prefix='PlateManager')
    current_backdrop = camUserVal.value
    
    try:
        backdrop = camera.itemGraph('shadeLoc').forward(0)
    except:
        backdrop = None
    else:
        # Save the backdrop id to the user value
        camera.setTag('LBBD', str(backdrop.id))
        
        # remove the back drop from the camera
        backdrop.itemGraph('shadeLoc').disconnectInput(camera)

def enable_backdrop(camera):
    """
    Enable the last assigned backdrop for a camera
    """
    
    camUserVal = UserValue(camera.id, prefix='PlateManager')
    try:
        backdrop = modo.Item(camera.getTags()['LBBD'])
    except LookupError as e:
        print 'No Backdrop found for camera: %s' % camera.id
    else:
        backdrop.itemGraph('shadeLoc').connectInput(camera)

def set_renderCam(camera, renderItem):
    """
    Set render camera and adjust frame range if camera has a clip attached
    """
    lx.eval('render.camera %s' % camera.id)
    set_range_from_clip(renderItem)
    
    
# Commands
arg = lx.args()[0]
if arg == 'setRange':
    set_range_from_clip(renderItem)
    
if arg == 'disableBackdrop':
    selected_cameras = scene.selectedByType(modo.c.CAMERA_TYPE)

    # disable the backdrop
    # if no camera is selected the current render cam is used
    if len(selected_cameras) == 0:
        disable_backdrop(scene.renderCamera)
    else:
        for camera in selected_cameras:
            disable_backdrop(camera)

if arg == 'enableBackdrop':
    selected_cameras = scene.selectedByType(modo.c.CAMERA_TYPE)

    # enable the backdrop
    # if no camera is selected the current render cam is used
    if selected_cameras:
        enable_backdrop(scene.renderCamera)
    else:
        for camera in selected_cameras:
            enable_backdrop(camera)

if arg == 'createProxy':
    files = scene.selectedByType(lx.symbol.sITYPE_VIDEOSEQUENCE)
    
    # If there is nothing selected we promt a file browser for the user
    # to set a directory for the files for us
    if not files:
        try:
            file_path = modo.dialogs.dirBrowse('Image Sequence Path', path=filename)
        except:
            print 'Abort'
        else:        
            files = _find_files(file_path, wildcard='#')
    
    status = modo.dialogs.okCancel('Creating Proxies', 'Creating proxies for following files:\n%s' % '\n'.join(files))
    if status == 'ok':
        for fp in files:
            create_proxy(fp, file_type='JPG', force=True)
    
if arg == 'createShotsub':
    try:
        file_path = modo.dialogs.dirBrowse('Image Sequence Path', path=filename)
    except:
        print 'Abort'
    else:
        files = _find_files(file_path)        
        status = modo.dialogs.okCancel('Creating Shotsub', 'Creating Shotssub(s) for:\n%s' % '\n'.join(files))
        if status == 'ok':
            for f in files:
                create_video(f)

if arg == 'setRenderCamera':
    camera = scene.selectedByType(modo.constants.CAMERA_TYPE)[0]
    if camera:
        set_renderCam(camera, renderItem)