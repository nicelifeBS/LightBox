import modo
import lx

def execute(Preview):
    ImgSrv = lx.service.Image()
    colorService = lx.service.ColorMapping()
    TosRGB = lx.object.ColorMapping(colorService.MakeColorMapping("nuke-default:sRGB", 0))
    
    width = 1000
    height = 800
    
    # Create preview and render
    Preview.Stop()    
    Preview.SetRes(width, height)
    lx.out(Preview.IsComplete())
    seconds = 20.0
    #RenderTimer = Timer(seconds, Preview.Stop())
    
    lx.out('Starting Render')
    #Preview.Reset()
    #Preview.Start()
