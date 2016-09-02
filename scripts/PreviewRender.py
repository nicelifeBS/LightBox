#python

import modo
import lx
import os

render_item = modo.scene.current().renderItem
scene = modo.Scene()

# get first, last and step from render item
first = render_item.channel(lx.symbol.sICHAN_POLYRENDER_FIRST).get()
last = render_item.channel(lx.symbol.sICHAN_POLYRENDER_LAST).get()
step = render_item.channel(lx.symbol.sICHAN_POLYRENDER_STEP).get()

def render(file_path, frames):
    '''
    Renders with modo offline renderer
    :param frames: list of frames
    '''
    
    file_path = os.path.splitext(file_path)

    # We go through our frames and set first and last frame to the same value
    # and then render this frame
    for frame in frames:
        render_item.channel(lx.symbol.sICHAN_POLYRENDER_FIRST).set(frame)
        render_item.channel(lx.symbol.sICHAN_POLYRENDER_LAST).set(frame)
        render_item.channel(lx.symbol.sICHAN_POLYRENDER_STEP).set(1)
        lx.eval('render.animation {%s} %s' % (file_path[0], file_path[1].upper()))
    
    # Here we reset the changed values to their defaults
    render_item.channel(lx.symbol.sICHAN_POLYRENDER_FIRST).set(first)
    render_item.channel(lx.symbol.sICHAN_POLYRENDER_LAST).set(last)
    render_item.channel(lx.symbol.sICHAN_POLYRENDER_STEP).set(step)

arg = lx.args()[0]
if arg == 'firstmiddlelast':
    """
    Render first middle and last frames of a sequence
    """

    # create the middle frame and sort and
    # delete duplicates in frame list
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
    """
    Render a sequence n frames. E.g. sequence 1-20 and number 10 will render
    only every second frame of the sequence.
    """

    frames = range(first, last+1)
    # for some reason we need to substract one from the number of frames
    number = lx.eval('user.value LIGHTBOX_renderFrames_number ?') -1
    frames = frames[::frames[-1]/number]    
    try:
        file_path = modo.dialogs.fileSave('image', 'png', title='Save Render', path=None)
    except:
        lx.out('Abort')
    else:    
        render(file_path, frames)