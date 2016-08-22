#python


import lxifc


import lx
import modo
from threading import Timer
import time

from PySide.QtCore import QTimer


lxifc.PreviewNotifier

lx.object.PreviewNotifier
lx.object.Preview

"""
THIS TOTALLY WORKS!!!

import modo
import lx

from PySide.QtCore import QTimer

preview = lx.service.Preview().CreatePreview()
timer = QTimer()
#preview.GetCurrentTime()
#preview.Reset()
preview.SetRes(1000, 1000)
def start():
	lx.out('Start')
	#preview.Start()
	preview.Reset()
	timer.timeout.connect(on_timer_callback)
	timer.start(5000)

def on_timer_callback():
	lx.out('Stop')
	preview.Stop()
	timer.stop()
	test(preview, ImgSrv, TosRGB)
	lx.out('DONE: ', preview.IsComplete())

def test(Preview, ImgSrv, TosRGB):
    previewImage = Preview.GetBuffer()
    w, h = previewImage.Size()
    ch = previewImage.Components()

    # create a new storage object for our pixels
    Pixel = lx.object.storage()
    Pixel.setType('f')
    Pixel.setSize(w * h * ch)

    # Create a new image for export
    exportImage = ImgSrv.Create(w, h, lx.symbol.iIMP_RGBAFP, 0)
    imWrite = lx.object.ImageWrite(exportImage)

    for ih in range(h):
        for iw in range(w):
            previewImage.GetPixel(iw, ih, lx.symbol.iIMP_RGBAFP, Pixel)
            iR = Pixel[0]
            iG = Pixel[1]
            iB = Pixel[2]
            # convert to sRGB
            R, G, B = TosRGB.FromLinear((iR, iG, iB), 3)
            # set the RGBA pixels
            imWrite.SetPixel(iw, ih, lx.symbol.iIMP_RGBAFP, Pixel)
            Pixel.set((R, G, B, Pixel[3]))

    ImgSrv.Save(imWrite, '/Users/bjoern_siegert/GitHub/LightBox/tests/test1.png', 'PNG', 0)

ImgSrv = lx.service.Image()
colorService = lx.service.ColorMapping()
TosRGB = lx.object.ColorMapping(colorService.MakeColorMapping("nuke-default:sRGB", 0))

start()
"""


def test(Preview, ImgSrv, TosRGB):
    previewImage = Preview.GetBuffer()
    w, h = previewImage.Size()
    ch = previewImage.Components()

    # create a new storage object for our pixels
    Pixel = lx.object.storage()
    Pixel.setType('f')
    Pixel.setSize(w * h * ch)

    # Create a new image for export
    exportImage = ImgSrv.Create(w, h, lx.symbol.iIMP_RGBAFP, 0)
    imWrite = lx.object.ImageWrite(exportImage)

    for ih in range(h):
        for iw in range(w):
            previewImage.GetPixel(iw, ih, lx.symbol.iIMP_RGBAFP, Pixel)
            iR = Pixel[0]
            iG = Pixel[1]
            iB = Pixel[2]
            # convert to sRGB
            R, G, B = TosRGB.FromLinear((iR, iG, iB), 3)
            # set the RGBA pixels
            Pixel.set((R, G, B, Pixel[3]))
            imWrite.SetPixel(iw, ih, lx.symbol.iIMP_RGBAFP, Pixel)	

    ImgSrv.Save(imWrite, '/Users/bjoern_siegert/Projects_local/TrollBridge/shots/tmp/test1.png', 'PNG', 0)


ImgSrv = lx.service.Image()
colorService = lx.service.ColorMapping()
TosRGB = lx.object.ColorMapping(colorService.MakeColorMapping("nuke-default:sRGB", 0))

width = 1000
height = 800

# Create preview and render
Preview = lx.service.Preview().CreatePreview()
Preview.SetRes(width, height)

def Stop():
    Preview.Stop()


seconds = 20.0
#RenderTimer = Timer(seconds, Preview.Stop())

lx.out('Starting Render')
Preview.Reset()
Preview.Start()

QTimer.singleShot(seconds, Stop)
#RenderTimer.start()
#print Preview.IsComplete()

#tn = time.time()
#tf = tn + seconds + 1.0
#rendering = True
#start = tn
#while rendering:
    #tn = time.time()
    #if tn >= tf:
        #rendering = False
        #lx.out('Stopping Render')
        #Preview.Stop()
        #break
#lx.out(int(tn) - int(start))
#lx.out('Render Status: ', Preview.IsComplete())

#print 'DONE'
#test(Preview, lx, ImgSrv, TosRGB)


