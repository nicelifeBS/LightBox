#python

import modo
import lx
import os

RenderItem = modo.scene.current().renderItem

# get first, last and step from render item
first = RenderItem.channel(lx.symbol.sICHAN_POLYRENDER_FIRST).get()
last = RenderItem.channel(lx.symbol.sICHAN_POLYRENDER_LAST).get()
step = RenderItem.channel(lx.symbol.sICHAN_POLYRENDER_STEP).get()

def render(file_path, frames):
    '''
    :param frames: list of frames
    '''
    
    file_path = os.path.splitext(file_path)

    for frame in frames:
        RenderItem.channel(lx.symbol.sICHAN_POLYRENDER_FIRST).set(frame)
        RenderItem.channel(lx.symbol.sICHAN_POLYRENDER_LAST).set(frame)
        RenderItem.channel(lx.symbol.sICHAN_POLYRENDER_STEP).set(1)
        lx.eval('render.animation {%s} %s' % (file_path[0], file_path[1].upper()))
    
    # reset values to default
    RenderItem.channel(lx.symbol.sICHAN_POLYRENDER_FIRST).set(first)
    RenderItem.channel(lx.symbol.sICHAN_POLYRENDER_LAST).set(last)
    RenderItem.channel(lx.symbol.sICHAN_POLYRENDER_STEP).set(step)

arg = lx.args()[0]
if arg == 'firstmiddlelast':
    
    # create the middle frame and sort and delete duplicates in
    # frame list
    frameRange = range(first, last+1)
    middle = frameRange[len(frameRange)/2]
    frames = list(set([first, middle, last]))
    
    try:
        file_path = modo.dialogs.fileSave('image', 'png', title='Save Render', path=None)
    except:
        print 'Abort'
    else:
        render(file_path, frames)

if arg == 'xframes':
    frames = range(first, last+1)
    # for some reason we need to substract one from the number of frames
    number = lx.eval('user.value LIGHTBOX_renderFrames_number ?') -1
    frames = frames[::frames[-1]/number]    
    try:
        file_path = modo.dialogs.fileSave('image', 'png', title='Save Render', path=None)
    except:
        print 'Abort'
    else:    
        render(file_path, frames)
    

