#!/usr/bin/env python

import lx
import lxu.command
import modo
import os

from PySide.QtCore import QTimer

# test: lightbox.renderprev /Users/bjoern_siegert/GitHub/_modo_kits/LightBox/tests/test123234234.png 500 500 timeout:500

class RenderPrev(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        # Create arguments
        self.dyna_Add('filepath', lx.symbol.sTYPE_STRING)   # 0
        self.dyna_Add('width', lx.symbol.sTYPE_INTEGER)     # 1
        self.dyna_Add('height', lx.symbol.sTYPE_INTEGER)    # 2
        self.dyna_Add('timeout', lx.symbol.sTYPE_INTEGER)   # 3
        self.dyna_Add('rendertime', lx.symbol.sTYPE_FLOAT)  # 4
        self.dyna_Add('format', lx.symbol.sTYPE_STRING)     # 5

        # Set optional flags
        self.basic_SetFlags(5, lx.symbol.fCMDARG_OPTIONAL)

        # Create a preview instance
        self.preview = lx.service.Preview().CreatePreview()

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def cmd_Interact(self):
        pass

    def basic_Execute(self, msg, flags):

        # Create a timer and connect it to our callback function
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_callback)

        # Get arguments from command
        self.file_path = self.dyna_String(0)
        width = self.dyna_Int(1)
        height = self.dyna_Int(2)
        timeout = self.dyna_Int(3)
        render_time = self.dyna_Float(4)
        self.img_format = self.dyna_String(5, 'PNG')

        self.preview.SetRes(width, height)

        # prepare filename
        self.preview.Reset()
        self.preview.SetRenderTime(render_time)
        self.timer.start(timeout)
        self.preview.Start()
        lx.out('START')

    def on_timer_callback(self):
        """
        Callback function triggered by timer
        """
        lx.out('STOP')
        self.timer.stop()
        self.preview.Stop()
        self.save_render()

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()

    def save_render(self):
        """
        Save frame buffer as image. We convert input buffer to sRGB before it is
        written to disk
        """

        # We need an image and a color service to save the image and
        # apply a sRGB LUT to the linear color values
        img_srv = lx.service.Image()
        color_service = lx.service.ColorMapping()
        to_srgb = lx.object.ColorMapping(color_service.MakeColorMapping("nuke-default:sRGB", 0))

        # Get the image buffer from the renderer
        buffer = self.preview.GetBuffer()
        w, h = buffer.Size()
        ch = buffer.Components()

        # create a new storage object for our pixels
        pixel = lx.object.storage()
        pixel.setType('f')
        pixel.setSize(w * h * ch)

        # Create a new image for export
        export_image = img_srv.Create(w, h, lx.symbol.iIMP_RGBAFP, 0)
        img_output = lx.object.ImageWrite(export_image)

        # Iterate over pixels and convert them into sRGB
        for ih in range(h):
            for iw in range(w):
                buffer.GetPixel(iw, ih, lx.symbol.iIMP_RGBAFP, pixel)
                iR = pixel[0]
                iG = pixel[1]
                iB = pixel[2]
                # convert to sRGB
                R, G, B = to_srgb.FromLinear((iR, iG, iB), 3)
                # set the RGBA pixels
                img_output.SetPixel(iw, ih, lx.symbol.iIMP_RGBAFP, pixel)
                pixel.set((R, G, B, pixel[3]))

        # Save the image to disk
        img_srv.Save(img_output, self.file_path, self.img_format, 0)

lx.bless(RenderPrev, "lightbox.renderprev")