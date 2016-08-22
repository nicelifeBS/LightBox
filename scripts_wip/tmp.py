
camera.channelNames
print dir(camera)

for c in camera.iterChannels():
    print c.isAnimated, c.index, c.type
    break

#?key.scale 0.1 start 0.0 input false

2.0/120
frames = 3
frame_range = scene.sceneRange
start = frame_range[0]
lx.eval('key.scale %s start %s input false' % ( (frames-1.0)/frame_range[1], start ) )




import lx
import modo

scene = modo.scene.current()
camera = scene.selectedByType(lx.symbol.sITYPE_CAMERA)[0]

scene.deselect()
scene.select(camera)

lx.eval('select.drop envkey')
#select.keyRange rotation005 4 -1.409 0.302 mode:add

selection_service = lx.service.Selection()
chan_sel_type = selection_service.LookupType(lx.symbol.sSELTYP_CHANNEL)

# decode selection packets into channel packets to transcode information
chan_transpacket = lx.object.ChannelPacketTranslation(selection_service.Allocate(lx.symbol.sSELTYP_CHANNEL))

# get the number of selected channels
chan_n = selection_service.Count(chan_sel_type)

# iterate over all our packets and extract the information we need
for x in xrange(chan_n):
    packet_pointer = selection_service.ByIndex(chan_sel_type, x)
    if not packet_pointer:
        lx.out('Bad selection packet, skipping...')
        continue

    item = lx.object.Item(chan_transpacket.Item(packet_pointer))
    chan_idx = chan_transpacket.Index(packet_pointer)

    # Show selection info in Event Log
    print '%s : %s' % (item.Ident(), chan_idx)



