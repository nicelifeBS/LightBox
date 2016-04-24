#python

import modo
import lx

scene = modo.scene.current()

# This is now deprecated we use the create_from_preset now
def create_light(name=None, type='areaLight'):

    if not name:
        # Create temp user value and ask user
        # for light name        
        lx.eval('user.defNew LightCreate.name type:string life:momentary')
        lx.eval('user.value LightCreate.name value:AreaLight')
        lx.eval('user.def LightCreate.name dialogname "Light Name"')
        lx.eval('user.value LightCreate.name')
        name = lx.eval('user.value LightCreate.name ?')

    s = []
    lx.eval('item.create locator name:%s_LOC' % name)
    s += scene.selectedByType(modo.constants.LOCATOR_TYPE)
    lx.eval('item.create areaLight name:%s_AL' % name)
    s += scene.selectedByType(modo.constants.AREALIGHT_TYPE)

    if len(s) == 2:
        lx.eval('item.parent %s %s 0 inPlace:1' % (s[1].id, s[0].id))

        # create direction constrain
        scene.select(s[1])
        scene.select(s[0], add=True)		
        lx.eval('constraintDirection')


def create_from_preset(scene, preset_path, name=None):
    '''Create a new light from a preset'''
    
    # we need to deselect all items to reduce a mess
    scene.deselect()

    # Create temp user value and ask user
    # for light name            
    if not name:
        lx.eval('user.defNew LightBox.areaLight type:string life:momentary')
        lx.eval('user.value LightBox.areaLight value:AreaLight')
        lx.eval('user.def LightBox.areaLight dialogname "Light Name"')
        lx.eval('user.value LightBox.areaLight')
        name = lx.eval('user.value LightBox.areaLight ?')
    
    # renaming of locator and its light
    if name:
        # create light from preset
        lx.eval('preset.do %s' % preset_path)        

        Loc = scene.selectedByType(modo.c.LOCATOR_TYPE)[0]
        Light = Loc.children()[0]
        Loc.name = '%s_LOC' % name
        Light.name = '%s_LIGHT' % name   


# Absolute file path of Lightbox
FileService = lx.service.File()
kit_path = FileService.ToLocalAlias('kit_LightBox:')

args = lx.args()[0]
if args == 'areaLight':
    from os import path
    preset_path = path.join(kit_path, 'assemblies/areaLightRig.lxp')
    create_from_preset(scene, preset_path)