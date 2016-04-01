#python

import modo
import lx
from collections import namedtuple

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


# Commands
arg = lx.args()[0]
if arg == 'setRange':
    set_range_from_clip()
if arg == 'disableBackdrop':
    pass