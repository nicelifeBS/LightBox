import modo
import lx

scene = modo.scene.current()

# go through all environments and find missing textures
errors = []
for img in scene.items(itype=lx.symbol.sITYPE_IMAGEMAP):
    try:
        shade_loc = img.itemGraph('shadeLoc').forward(1)
    except:
        errors.append(img)

for img in scene.items(itype=lx.symbol.sITYPE_VIDEOCLIP):
    try:
        shade_loc = img.itemGraph('shadeLoc').forward(1)
    except:
        errors.append(img)

# Deselect everything first and then select all
# bad images in scene
scene.deselect()
for e in errors:
    scene.select(e, add=True)